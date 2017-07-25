# Varnish Configuration File
#
# See the VCL chapters in the Users Guide at https://www.varnish-cache.org/docs/
# and https://www.varnish-cache.org/trac/wiki/VCLExamples for more examples.

# Marker to tell the VCL compiler that this VCL has been adapted to the
# new 4.0 format.
vcl 4.0;

backend default {
     .host = "localhost";
     .port = "8080";
}

sub vcl_recv {
    # Happens before we check if we have this in cache already.
    #
    # Typically you clean up the request here, removing cookies you don't need,
    # rewriting the request, etc.

    if ((req.url ~ ".php") || (req.url ~ ".cgi") || (req.url ~ ".sh")) {
       return (synth(404, "Not Found."));
    }

    if (req.url ~ ".jsp") {
       return (synth(404, "Not Found."));
    }

    # Allow PURGE with special header only
    if (req.method == "PURGE") {
       if (req.http.quijibo) {
         return (purge);
       }
       return (synth(405, "Not allowed."));
    }

    # Don't cache anything on Admin
    # Don't cache puts or posts
    if (req.url ~ "^/josh/") {
        return (pass);
    }

    if (req.method == "PUT") {
        return (pass);
    }

    if (req.method == "POST") {
        return (pass);
    }


    if (!(req.url ~ "^/josh/")) {
        # Remove All incoming cookies for any route not josh (need csrf token cookies for admin)
        set req.url = regsub(req.url, "\?.*$", "");
        set req.http.Host = regsub(req.http.Host, ":[0-9]+", "");
        unset req.http.Cookie;
        unset req.http.Cache-Control;
        unset req.http.Accept-Encoding;
        unset req.http.User-Agent;
        unset req.http.Accept-Language;
        unset req.http.Upgrade-Insecure-Requests;
        unset req.http.Origin;
        unset req.http.X-Requested-With;
        unset req.http.X-CSRFToken;
        unset req.http.If-Modified-Since;

        # Ignore all of the different ways various browsers and devices send accept-encoding.
        if (req.http.Accept-Encoding) {
            if (req.http.Accept-Encoding ~ "gzip") {
              set req.http.Accept-Encoding = "gzip";
            } else if (req.http.Accept-Encoding ~ "deflate") {
              set req.http.Accept-Encoding = "deflate";
            } else {
              unset req.http.Accept-Encoding;
            }
        }

        return(hash);
    }
}

sub vcl_hash {
    # Override the hash and only store hashed items with the url key
    hash_data(req.url);
    return (lookup);
}

sub vcl_backend_response {
    # Happens after we have read the response headers from the backend.
    #
    # Here you clean the response headers, removing silly Set-Cookie headers
    # and other mistakes your backend does.

    # Remove cookies that destroy cache - you can't ignore my cache!
    if (!(bereq.url ~ "^/admin/")) {
       unset beresp.http.Set-Cookie;
       unset beresp.http.Server;
       unset beresp.http.X-Powered-By;
       unset beresp.http.Vary;
    }

    # only cache status ok
    if ( beresp.status != 200 ) {
        set beresp.uncacheable = true;
        set beresp.ttl = 120s;
        return (deliver);
    }
     #else {
     #   if (bereq.url ~ "^/api/v1/config") {
     #      set beresp.ttl = 86400s;
     #   }
     # }
}

sub vcl_deliver {
    # Happens when we have all the pieces we need, and are about to send the
    # response to the client.
    #
    # You can do accounting or modifying the final object here.

    # Was a HIT or a MISS?
    if ( obj.hits > 0 ) {
        set resp.http.X-Cache = "HIT";
    } else {
        set resp.http.X-Cache = "MISS";
    }

    # And add the number of hits in the header:
    set resp.http.X-Cache-Hits = obj.hits;
}

