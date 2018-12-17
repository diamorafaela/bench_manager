// Copyright (c) 2018, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Campos ocultos', {
	sitio: function(frm){
		sitio_func(frm);
	},
	doctype_ex: function(frm){
		doctype_ex_func(frm);
	},	
	refresh: function(frm) {
		if(frm.fields_dict.sitio.get_value()){
			sitio_func(frm);
		}
		if(frm.fields_dict.doctype_ex.get_value()){
			doctype_ex_func(frm);
		}
	},
});
frappe.ui.form.on('Campos ocultos campos', {
	campo: function(frm, cdt, cdn){
		campo_func(frm, cdt, cdn)
	},
	campos_add: function(frm){
		doctype_ex_func(frm);
	},
});
function campo_func(frm,cdt,cdn){
	frappe.call({
		method: "bench_manager.api.get_hidden", 
		args: { 
				site: frm.fields_dict.sitio.get_value(), 
				doc: frm.fields_dict.doctype_ex.get_value(), 
				campo: frm.fields_dict["campos"].grid.grid_rows_by_docname[cdn].get_field("campo").get_value() 
			  },
		callback: function(r){
			if(r.message){
				frm.fields_dict["campos"].grid.grid_rows_by_docname[cdn].get_field("oculto").set_value(r.message)
			}
		}
	});
}
function doctype_ex_func(frm){
	frappe.call({method: "bench_manager.api.get_campos_doc", args: { site: frm.fields_dict.sitio.get_value(), doc: frm.fields_dict.doctype_ex.get_value() },
	callback: function(r){
		if(r.message){
			for(var a in cur_frm.fields_dict["campos"].grid.grid_rows_by_docname){
				frappe.utils.filter_dict(cur_frm.fields_dict["campos"].grid.grid_rows_by_docname[a].docfields, {"fieldname": "campo"})[0].options=r.message;
				//cur_frm.fields_dict["campos"].grid.grid_rows_by_docname[a].get_field("campo").refresh();
			}
		}
	}});
}
function sitio_func(frm){
	frappe.call({method: "bench_manager.api.get_site_docs", args: { site: frm.fields_dict.sitio.get_value() },
	callback: function(r){
		if(r.message){
			frm.set_df_property('doctype_ex', 'options', r.message.split('\n'));
			frm.refresh_field('doctype_ex');
		}
	}})
}
