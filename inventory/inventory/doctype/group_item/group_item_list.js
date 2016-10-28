frappe.listview_settings['Group Item'] = {
	add_fields: ["status_group"],
	get_indicator: function(doc) {
        if(doc.status_group === "Unused"){
        	return [__("Unused"), "grey", "status_group,=,Unused"];

        }
        else if(doc.status_group === "Partly Used"){
        	return [__("Partly Used"), "orange", "status_group,=,Partly Used"];

        }
        else if(doc.status_group === "Complete Used"){
        	return [__("Complete Used"), "green", "status_group,=,Complete Used"];

        } 
	}
};
