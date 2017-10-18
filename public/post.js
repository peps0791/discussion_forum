/*name: post.js*/
/*description: javascript code for all posts files.*/
/*author: ppapreja*/

/*TO-DO*/
/*1. implement ajax request for comment posting.*/

/*implements popover opening on comment button click.*/
$(".comment-btn").popover({

    title: '<h3 class="custom-title"><span class="glyphicon glyphicon-info-sign"></span> You\'re almost there!</h3>',
    content : function(){
    	
    	var commentbtnid = this.id;
    	console.log('from inside popover for id -->' +commentbtnid);
    	//check for similarity
    	//extract text from text area
		var id = commentbtnid.substring(commentbtnid.lastIndexOf('-')+1);

		commentid = id;
		console.log('commentid-->' +commentid)
		var textareaid = 'speech-'+id;
		console.log('text area id-->' +textareaid);
		var text = $('#' + textareaid).val();
		console.log('text-->' +text);

		var blockedwords = ['thanks!!', 'thank you', '+1', 'me too!!', 'great!']
		for(var i=0;i<blockedwords.length;i++){

			var similarityresult = checkSimilarity(text, blockedwords[i]);
			console.log('similarity result to ' +  blockedwords[i] +' -->' +similarityresult)
			if(similarityresult>0.60){
				blockcomment = true;
				break;
			}
		}

  		console.log('block comment -->' + blockcomment)
    	if(blockcomment == false){

    		return "<div id = contentcheck><p id = 'okaytext' style = 'font-color:green;'>Looks OK</p></div> <div id = 'similaritydiv'><label><input  class = 'sample' id='similaritycheckbox' type='checkbox' /> Are you sure your comments isn't just a \"Me too!\", \"thanks\", or \"+1\"? </label></div><button type='button' id = 'postcmtbtn'  class='popovercomment btn btn-primary btn-block' onclick = \'publishcomment()\'>Post Question</button><div id = 'faqlink'><p>Here\'s some more info about posting questions.</p></div>"

    	}else{
    		return "<div id = contentcheck><p id = 'notokaytext' style = 'font-color:red;'>Fix Needed</p></div> <div id = 'similaritydiv'><label><input  class = 'sample' id='similaritycheckbox' type='checkbox' /> Are you sure your comments isn't just a \"Me too!\", \"thanks\", or \"+1\"? </label></div><button type='button' id = 'postcmtbtn'  class='popovercomment btn btn-primary btn-block' onclick = \'publishcomment()\'>Post Question</button><div id = 'faqlink'><p>Here\'s some more info about posting questions.</p></div>"
    	}	
    },
    html: true
}); 

/*final comment posting to be handled from within this function.*/
function publishcomment(){
	console.log('publish comment called');
}

/*populates resources (links extracted from the page into the resources window pane)*/
function populateResources(content){
    //var content = $('.content').html();
    //console.log('content' +content);
    var index = 0;
    
    startindex = 0;
    endindex = 0;

    var list = document.createElement('ul')
    var resourcestab = document.getElementById('resourcescontent')
    resourcestab.appendChild(list)

    while(startindex!=-1){

        startindex = content.indexOf("<a", index);
        console.log(startindex)

        if(startindex==-1){
            continue;
        }
        endindex = content.indexOf("</a>", startindex);
        console.log(endindex)
        var link = content.substring(startindex, endindex+1);
        console.log('link-->' +link)
        

        var el = document.createElement('li');
        list.appendChild(el);
        el.innerHTML = link;
        list.append(document.createElement('br'))

        index = endindex+1;
    }
}