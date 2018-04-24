(function($) {
    $.ajax(base_url + "/api/v1/data", {
        success: function(hosts) {
            var hostlist_source = $("#host_list_template").html();
            var tmpl = Handlebars.compile(hostlist_source);
            var data = [];
            for (var i = 0; i < hosts.length; i++) {
            	var host_groups = hosts[i]["host_groups"];
            	for (var j = 0; j < host_groups.length; j++) {
            		var name = host_groups[j]["name"];
            		if (name in data) {
            			data[name]["hosts"].push(hosts[i]);
            		} else {
	            		data[name] = {
	            			alias: host_groups[j]["alias"],
	            			hosts: [hosts[i]]
	            		};
            		}
            	}
            }
            console.log(data);
            $("#hosts").html(tmpl({ hosts: hosts, host_groups: data }));

        }
    });
})(jQuery);
