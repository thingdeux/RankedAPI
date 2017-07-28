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
    # START - NASTY BLOCK OF USER-AGENT / BOT blocks
    if (
         req.http.user-agent ~ "^$"
      || req.http.user-agent ~ "^Java"
      || req.http.user-agent ~ "^Jakarta"
      || req.http.user-agent ~ "IDBot"
      || req.http.user-agent ~ "id-search"
      || req.http.user-agent ~ "User-Agent"
      || req.http.user-agent ~ "compatible ;"
      || req.http.user-agent ~ "ConveraCrawler"
      || req.http.user-agent ~ "^Mozilla$"
      || req.http.user-agent ~ "libwww"
      || req.http.user-agent ~ "lwp-trivial"
      || req.http.user-agent ~ "curl"
      || req.http.user-agent ~ "PHP/"
      || req.http.user-agent ~ "urllib"
      || req.http.user-agent ~ "GT:WWW"
      || req.http.user-agent ~ "Snoopy"
      || req.http.user-agent ~ "MFC_Tear_Sample"
      || req.http.user-agent ~ "HTTP::Lite"
      || req.http.user-agent ~ "PHPCrawl"
      || req.http.user-agent ~ "URI::Fetch"
      || req.http.user-agent ~ "Zend_Http_Client"
      || req.http.user-agent ~ "http client"
      || req.http.user-agent ~ "PECL::HTTP"
      || req.http.user-agent ~ "panscient.com"
      || req.http.user-agent ~ "IBM EVV"
      || req.http.user-agent ~ "Bork-edition"
      || req.http.user-agent ~ "Fetch API Request"
      || req.http.user-agent ~ "PleaseCrawl"
      || req.http.user-agent ~ "[A-Z][a-z]{3,} [a-z]{4,} [a-z]{4,}"
      || req.http.user-agent ~ "layeredtech.com"
      || req.http.user-agent ~ "WEP Search"
      || req.http.user-agent ~ "Wells Search II"
      || req.http.user-agent ~ "Missigua Locator"
      || req.http.user-agent ~ "ISC Systems iRc Search 2.1"
      || req.http.user-agent ~ "Microsoft URL Control"
      || req.http.user-agent ~ "Indy Library"
      || req.http.user-agent == "8484 Boston Project v 1.0"
      || req.http.user-agent == "Atomic_Email_Hunter/4.0"
      || req.http.user-agent == "atSpider/1.0"
      || req.http.user-agent == "autoemailspider"
      || req.http.user-agent == "China Local Browse 2.6"
      || req.http.user-agent == "ContactBot/0.2"
      || req.http.user-agent == "ContentSmartz"
      || req.http.user-agent == "DataCha0s/2.0"
      || req.http.user-agent == "DataCha0s/2.0"
      || req.http.user-agent == "DBrowse 1.4b"
      || req.http.user-agent == "DBrowse 1.4d"
      || req.http.user-agent == "Demo Bot DOT 16b"
      || req.http.user-agent == "Demo Bot Z 16b"
      || req.http.user-agent == "DSurf15a 01"
      || req.http.user-agent == "DSurf15a 71"
      || req.http.user-agent == "DSurf15a 81"
      || req.http.user-agent == "DSurf15a VA"
      || req.http.user-agent == "EBrowse 1.4b"
      || req.http.user-agent == "Educate Search VxB"
      || req.http.user-agent == "EmailSiphon"
      || req.http.user-agent == "EmailWolf 1.00"
      || req.http.user-agent == "ESurf15a 15"
      || req.http.user-agent == "ExtractorPro"
      || req.http.user-agent == "Franklin Locator 1.8"
      || req.http.user-agent == "FSurf15a 01"
      || req.http.user-agent == "Full Web Bot 0416B"
      || req.http.user-agent == "Full Web Bot 0516B"
      || req.http.user-agent == "Full Web Bot 2816B"
      || req.http.user-agent == "Guestbook Auto Submitter"
      || req.http.user-agent == "Industry Program 1.0.x"
      || req.http.user-agent == "ISC Systems iRc Search 2.1"
      || req.http.user-agent == "IUPUI Research Bot v 1.9a"
      || req.http.user-agent == "LARBIN-EXPERIMENTAL (efp@gmx.net)"
      || req.http.user-agent == "LetsCrawl.com/1.0 +http://letscrawl.com/"
      || req.http.user-agent == "Lincoln State Web Browser"
      || req.http.user-agent == "LMQueueBot/0.2"
      || req.http.user-agent == "LWP::Simple/5.803"
      || req.http.user-agent == "Mac Finder 1.0.xx"
      || req.http.user-agent == "MFC Foundation Class Library 4.0"
      || req.http.user-agent == "Microsoft URL Control - 6.00.8xxx"
      || req.http.user-agent == "Missauga Locate 1.0.0"
      || req.http.user-agent == "Missigua Locator 1.9"
      || req.http.user-agent == "Missouri College Browse"
      || req.http.user-agent == "Mizzu Labs 2.2"
      || req.http.user-agent == "Mo College 1.9"
      || req.http.user-agent == "Mozilla/2.0 (compatible; NEWT ActiveX; Win32)"
      || req.http.user-agent == "Mozilla/3.0 (compatible; Indy Library)"
      || req.http.user-agent == "Mozilla/4.0 (compatible; Advanced Email Extractor v2.xx)"
      || req.http.user-agent == "Mozilla/4.0 (compatible; Iplexx Spider/1.0 http://www.iplexx.at)"
      || req.http.user-agent == "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT; DigExt; DTS Agent"
      || req.http.user-agent == "Mozilla/4.0 efp@gmx.net"
      || req.http.user-agent == "Mozilla/5.0 (Version: xxxx Type:xx)"
      || req.http.user-agent == "MVAClient"
      || req.http.user-agent == "NameOfAgent (CMS Spider)"
      || req.http.user-agent == "NASA Search 1.0"
      || req.http.user-agent == "Nsauditor/1.x"
      || req.http.user-agent == "PBrowse 1.4b"
      || req.http.user-agent == "PEval 1.4b"
      || req.http.user-agent == "Poirot"
      || req.http.user-agent == "Port Huron Labs"
      || req.http.user-agent == "Production Bot 0116B"
      || req.http.user-agent == "Production Bot 2016B"
      || req.http.user-agent == "Production Bot DOT 3016B"
      || req.http.user-agent == "Program Shareware 1.0.2"
      || req.http.user-agent == "PSurf15a 11"
      || req.http.user-agent == "PSurf15a 51"
      || req.http.user-agent == "PSurf15a VA"
      || req.http.user-agent == "psycheclone"
      || req.http.user-agent == "RSurf15a 41"
      || req.http.user-agent == "RSurf15a 51"
      || req.http.user-agent == "RSurf15a 81"
      || req.http.user-agent == "searchbot admin@google.com"
      || req.http.user-agent == "ShablastBot 1.0"
      || req.http.user-agent == "snap.com beta crawler v0"
      || req.http.user-agent == "Snapbot/1.0"
      || req.http.user-agent == "sogou develop spider"
      || req.http.user-agent == "Sogou Orion spider/3.0(+http://www.sogou.com/docs/help/webmasters.htm#07)"
      || req.http.user-agent == "sogou spider"
      || req.http.user-agent == "Sogou web spider/3.0(+http://www.sogou.com/docs/help/webmasters.htm#07)"
      || req.http.user-agent == "sohu agent"
      || req.http.user-agent == "SSurf15a 11"
      || req.http.user-agent == "TSurf15a 11"
      || req.http.user-agent == "Under the Rainbow 2.2"
      || req.http.user-agent == "User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
      || req.http.user-agent == "VadixBot"
      || req.http.user-agent == "WebVulnCrawl.blogspot.com/1.0 libwww-perl/5.803"
      || req.http.user-agent == "Wells Search II"
      || req.http.user-agent == "WEP Search 00"
      || req.http.user-agent == "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36 BBScan/1.1"
      || req.http.user-agent == "Mozilla/5.0 Jorgee"
    ) {
      return (synth(403, "Not allowed."));
    }

    # END - NASTY BLOCK
    # Block empty referrers
    if (req.http.user-agent ~ "^$" && req.http.referer ~ "^$") {
       return (synth(204, "No Content"));
    }

    # Happens before we check if we have this in cache already.
    #
    # Typically you clean up the request here, removing cookies you don't need,
    # rewriting the request, etc.

    if ((req.url ~ "\.php$") || (req.url ~ "\.cgi$") || (req.url ~ "\.sh$")) {
       return (synth(404, "Not Found B."));
    }

    if ((req.url ~ "\.jsp$") || (req.url ~ "\.aspx$")) {
       return (synth(404, "Not Found A."));
    }

    if ((req.url ~ "^/api/v1/users/me/$") || (req.url ~ "^/api/v1/videos/$")) {
       return (pass);
    }

    # Allow PURGE with special header only
    if (req.method == "PURGE") {
       if (req.http.quijibo) {
         return (purge);
       }
       return (synth(405, "Not allowed."));
    }

    # Don't cache anything on Josh Endpoint
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
        # set req.url = regsub(req.url, "\?.*$", "");
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
    if (!(bereq.url ~ "^/josh/")) {
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

