$(function () { 
	var g;// = new Bluff.StackedBar('graph', 400); 

	function drawGraph(data) { 
	    g = new Bluff.StackedBar('graph', 400); 

	    g.theme_pastel(); 
	    g.title = "EBP Data"; 
	    
	    g.data("No", data['No']); 
	    g.data("Yes", data['Yes']); 
	    
	    g.labels = data['labels']; 
	    
	    g.draw();                                       
	}; 

	function showSpinner() {
	    $('#graph').hide();
	    $('#spinner').show();
	};

	function hideSpinner() {
	    $('#spinner').hide();
	    $('#graph').show();
	};

	function updateData() {
	    $.getJSON("/summary/", function(data) {
		    hideSpinner();
		    drawGraph(data);
		});
	};

	function hideGraph() {
	    g.clear();
	    showSpinner();
	};

	var formOptions = {
	    beforeSubmit: hideGraph,
	    success: updateData,
	    clearForm: true,
	    resetForm: true
	};

	$('#ebpdata_form').ajaxForm(formOptions);

	updateData();
    });
