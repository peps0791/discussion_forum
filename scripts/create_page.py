import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
import re

folder = "../views/posts/";

def extractTagsFromObj(tags):
	#print 'original tags-->', tags
	tagsArr = []
	tagsArr = tags.split('>')
	newTagsArr = [tag.replace('<', '') for tag in tagsArr]
	
	newTagsArr = newTagsArr[:-1]
	#print 'formatted tags array-->', newTagsArr
	return newTagsArr;


def extractUserInfoFromPosts(root, userId):
	
	tagSortedDictionary = {'None':0};

	for child in root:
		postOwnerId = child.get('OwnerUserId');
		if userId == postOwnerId:

			tagsArr = []
			#get score and tag information and put them in a dictionary
			tags = child.get('Tags');
			if tags is not None:
				tagsArr = extractTagsFromObj(tags)

			#tags = str(tags).replace('<', '');
			#tags = str(tags).replace('>', '');
			score = child.get('Score');
			score = int(score);

			if tagsArr !=[]:
				for tag in tagsArr:
					if tag in tagSortedDictionary:
						tagSortedDictionary[tag] += score
					else:
						tagSortedDictionary[tag] = score
			else:
				tagSortedDictionary['None'] += score;

	return tagSortedDictionary



def createUserInfoHTML(displayname, reputation, quesId, tagSortedDictionary):

	userHTML = "\n\t\t\t<div class = \"userinfosection\"  id = \"userinfo-" + quesId +"\" data-toggle = \"popover\">" +\
				"\n\t\t\t\t<p>user name : " + displayname  + "</p>" +\
				"\n\t\t\t\t<p> user reputation : " + str(reputation) + "</p>" +\
				"\n\t\t\t\t<p class = \"tagcontent\" id = \"usertaginfo-" + quesId + "\">" +  str(tagSortedDictionary) + "</p>" +\
				"\n\t\t\t</div><br>"

	return userHTML;

def getUserInfoHTML(root, postRoot, userId, quesId):

	#print 'ID-->', userId, ' quesid-->', quesId
	if userId is not None:
		for child in root:
			currentUserId = child.get('Id');
			if currentUserId == userId:
				#get information of this user such as display name, reputation.
				displayName = child.get('DisplayName');
				#print 'display name -->', displayName
				reputation = child.get('Reputation');
				#print 'reputation -->', reputation
				break;
	else:
		displayName = 'None'
		reputation = 'NA'

	tagSortedDictionary = extractUserInfoFromPosts(postRoot, userId);

	#print tagSortedDictionary
	
	userInfoHTML = createUserInfoHTML(displayName, reputation, quesId, tagSortedDictionary);
	return userInfoHTML;

def createVoteHTML(id, views, score, isQues):
	votehtml = "\n\t\t\t<div id=\"vote-" + id + "\" class=\"upvote\" style=\"float:left;\">" +\
          	  "\n\t\t\t\t<a class=\"upvote\"></a>" +\
              "\n\t\t\t\t<span class=\"count\">" + score + "</span>" +\
              "\n\t\t\t\t<a class=\"downvote\"></a>" +\
              "\n\t\t\t\t<a class=\"star\"></a>";
	if isQues is 'True':
		votehtml+="\n\t\t\t\t<p>Views :: " + views +"</p>";
    
	votehtml+="\n\t\t\t</div>";
	return votehtml

def createAnswerHTML(id, answer, score):

	if score is None:
		score = '--'
	htmlContent = "\n\t\t\t<br><div id = \"ans-" + id + "\"  class = \"post\">" +\
	"\n\t\t\t\t<h2>Answer</h2>" +\
	createVoteHTML(id, "-1", score, 'False') +\
	"\n\t\t\t\t<p>" +answer+ "</p><br>" +\
	"\n\t\t\t</div>";
	return htmlContent

def createCommentHTML(id, comment):
	htmlContent = "\n\t\t\t<div id = \"comment-" +id + "\" class = \"comment\">" +\
	"\n\t\t\t\t<p>" +comment+ "</p>" +\
	"\n\t\t\t</div>";
	return htmlContent

def findComments(root, quesId):
	#print root
	#print quesId
	commentHeader = '<h3>Comments</h3>';
	commentStr = '';
	
	#div for containing comments
	parentdivStart = "\n\t\t\t<div id = \"commentsection-" +quesId + "\" class = 'collapse'>"
	for child in root:
		postId = child.get('PostId');
		if postId == quesId:
			id = child.get("Id");
			comment = child.get('Text');
			comment = re.sub(r'[^\x00-\x7F]+',' ', comment);
			commentStr  = commentStr + createCommentHTML(id, comment);

	parentdivEnd = "\n\t\t\t</div>";

	entercontent = "\n\t\t\t\t<textarea id = \"speech-"+quesId+"\" rows=\"3\" cols=\"80\"></textarea><br>" +\
	"\n\t\t\t\t<button class=\"record-start\" id=\"start-"+quesId+"\">"+\
	"\n\t\t\t\t\t<img id=\"start_img-" +quesId+"\" src=\"/mic.gif\" alt=\"Start\">" +\
	"\n\t\t\t\t</button>" +\
    "\n\t\t\t\t<button class = \"comment-btn\" id = \"comment-btn-" + quesId + "\">Comment</button>";
	if commentStr !="":
		#print 'some comments'
		loadCmtsButton = "\n\t\t\t\t<button data-toggle = 'collapse' data-target = \"#commentsection-" + quesId +"\">Load Comments</button></br>";
		commentStr = commentHeader + loadCmtsButton + parentdivStart + commentStr + parentdivEnd + entercontent; 
	else:
		#print 'no comments'
		#display label
		noCommentsLabel = '<p>no comments yet<p><br>'
		commentStr = commentHeader + noCommentsLabel + parentdivStart + commentStr + parentdivEnd + entercontent; 

	return commentStr


def findAnswers(root, commentRoot, quesId, userRoot):
	answerStr = '';
	for child in root:
		postTypeId = child.get('PostTypeId');
		if postTypeId != '1':
			#its an answer
			#see if its parent id matches the quesId
			parentId = child.get('ParentId')
			postId = child.get('Id');
			#print 'post id-->', postId
			if parentId == quesId:
				answer = child.get('Body')
				views = child.get('ViewCount')
				#print 'views-->', views
				score = child.get('Score')
				currentUserId = child.get('OwnerUserId')
				#print 'score-->', score
				answer = re.sub(r'[^\x00-\x7F]+',' ', answer)

				#find user info for this answer
				userInfoHTML = getUserInfoHTML(userRoot, root, currentUserId, postId)
				userInfoHTML = re.sub(r'[^\x00-\x7F]+',' ', userInfoHTML);

				#find comment for this answer
				commentStr = findComments(commentRoot, postId);
				answerStr = answerStr + createAnswerHTML(postId, answer, score) + userInfoHTML + commentStr;

	return answerStr


def createContent(title, id, body, userInfoHTML, score, views, comments, answerStr):

	content = "<html>"+ \
			  "\n\t<head>" + \
			  "\n\t\t<link href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u\" crossorigin=\"anonymous\">" +\
			  "\n\t\t<script src=\"https://code.jquery.com/jquery-3.2.1.min.js\" integrity=\"sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=\"  crossorigin=\"anonymous\"></script>" +\
			  "\n\t\t<script src = \"/jquery-highlight.js\"></script>" +\
			  "\n\t\t<link href=\"/jquery.upvote.css\" rel=\"stylesheet\">" +\
    		  "\n\t\t<script src = \"/jquery.upvote.js\" type=\"text/javascript\"></script>" +\
			  "\n\t\t<script src=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js\"></script>" +\
			  "\n\t\t<link rel=\"stylesheet\" href=\"/style.css\"/>" + \
			  "\n\t\t<script src=\"/createlinks.js\"></script>" + \
			  "\n\t\t<script src=\"/textaudit.js\"></script>" + \
			  "\n\t\t<script src=\"/PorterStemmer1980.min.js\"></script>" + \
			  "\n\t\t<script src=\"/highlight.js\"></script>" + \
			  "\n\t\t<title id = 'pagetitle'>"+title+ \
			  "\n\t\t</title>"+\
			  "\n\t</head>"+\
			  "\n\t<body id = 'pagebody'>"+ \
			  "\n\t\t<div id = \"loginmodals\"></div>" +\
    		  "\n\t\t<div id = \"issuemodals\"></div>" +\
    		  "\n\t\t<div id = \"highlight_tool\"></div>" +\
		  "\n\t\t<div id = \"comment_tool\"></div>" +\
			  "\n\t\t<div class = \"container\">" +\
			  "\n\t\t\t<header>" +\
			  "\n\t\t\t\t<h1>Just Another Discussion Forum</h1>" +\
			  "\n\t\t\t</header>" +\
			  "\n\t\t\t<div class=\"topnav\" id=\"myTopnav\">" + \
			  "\n\t\t\t\t<a href=\"/home\">Home</a>" + \
			  "\n\t\t\t\t<a href = \"#issueModal\" data-toggle=\"modal\" style = \"float:right\">Report Issue</a>" +\
			  "\n\t\t\t</div>" +\
			  "\n\t\t\t<div class = \"content\">" +\
			  "\n\t\t\t<div id = \"ques-" + id + "\" class = \"post\">" +\
			  "\n\t\t\t<h2>Question</h2>" +\
			  createVoteHTML(id, views, score, 'True') +\
			  "\n\t\t\t<form id = \"questionpostsform\" method=\"GET\" action = \"/ask\">" +\
          	  "\n\t\t\t\t<input type=\"submit\" id = \"quesbtn\" class=\"btn btn-primary btn-lg\" value=\"Ask Question\">" +\
        	  "\n\t\t\t</form>" +\
			  "\n\t\t\t\t<h2>" + title + "</h2>" +\
			  "\n"	+body+\
			  "\n\t\t\t</div>" +\
			  userInfoHTML +\
			  "\n\t\t\t<br>" +\
			  comments + \
			  "\n\n<h1>Answers</h1>" +\
			  answerStr +\
			  "\n\t\t\t</div>" +\
			  "\n\t\t\t<div id = \"resourcestab\" class = \"resourcestab\">" +\
			  "\n\t\t\t\t<ul class=\"nav nav-tabs\">" +\
          	  "\n\t\t\t\t\t<li class=\"active\"><a data-toggle=\"tab\" href=\"#resources\">Resources</a></li>" +\
          	  "\n\t\t\t\t\t<li><a data-toggle=\"tab\" href=\"#summary\">Summary</a></li>" +\
          	  "\n\t\t\t\t\t<li><a data-toggle=\"tab\" href=\"#highlights\">Highlights</a></li>" +\
        	  "\n\t\t\t\t</ul>" +\
        	  "\n\t\t\t\t\t<div class=\"tab-content\">" +\
              "\n\t\t\t\t\t\t<div id=\"resources\" class=\"tab-pane fade in active\">"+\
              "\n\t\t\t\t\t\t\t<h3>Links from the Page</h3>" +\
              "\n\t\t\t\t\t\t\t<div id = \"resourcescontent\"></div>" +\
          	  "\n\t\t\t\t\t\t</div>" +\
              "\n\t\t\t\t\t\t<div id=\"summary\" class=\"tab-pane fade\">" +\
              "\n\t\t\t\t\t\t\t<h3>Summary</h3>" +\
              "\n\t\t\t\t\t\t\t<div id = \"summarycontent\"></div>" +\
              "\n\t\t\t\t\t\t</div>" +\
              "\n\t\t\t\t\t\t<div id=\"highlights\" class=\"tab-pane fade\">" +\
              "\n\t\t\t\t\t\t\t<h3>Highlights</h3>" +\
              "\n\t\t\t\t\t\t\t<div id = \"highlightcontent\"></div>" +\
              "\n\t\t\t\t\t\t</div>" +\
			  "\n\t\t\t</div>" +\
			  "\n\t\t\t</div>" +\
			  "\n\t\t\t<footer>Moore & Peps collaboration.</footer>"+\
			  "\n\t</div>" +\
			  "\n\t<script src=\"/post.js\"></script>" +\
			  "\n\t<script type=\"text/javascript\">" +\
			  "\n\t\t$(\"#loginmodals\").load(\"/loginModal.html\");"+\
    		  "\n\t\t$(\"#issuemodals\").load(\"/issueModal.html\");" +\
    		  "\n\t\t$(\"#highlight_tool\").load(\"/highlight_tool.html\");" +\
		  "\n\t\t$(\"#comment_tool\").load(\"/comment_tool.html\");" +\
    		  "\n\t\tcheckLoggedInUser()" +\
			  "\n\t\tvar content = $('.content').html();" +\
			  "\n\t\tpopulateResources(content)" +\
			  "\n\t\tgetHighlights()" +\
			  "\n\t\tsetOnLinksHover()" +\
			  "\n\t</script>" +\
			  "\n\t<script src=\"/media.js\"></script>" +\
			  "\n\t<script src=\"/vote.js\"></script>" +\
			  "\n\t<script src=\"/managefunction.js\"></script>" +\
			  "\n\t</body>" +\
			  "\n</html>";

	return content


def main():

	tree = ET.parse('../data/robotics.stackexchange.com/Posts.xml');
	commentTree = ET.parse('../data/robotics.stackexchange.com/Comments.xml');
	userTree = ET.parse('../data/robotics.stackexchange.com/Users.xml');
	userRoot = userTree.getroot();
	commentRoot = commentTree.getroot();
	root = tree.getroot();
	for child in root:

		postTypeId = child.get('PostTypeId');
		if(postTypeId == '1'):
			#create separate page
			title = child.get('Title');
			title = re.sub(r'[^\x00-\x7F]+',' ', title);
			body = child.get('Body');
			body = re.sub(r'[^\x00-\x7F]+',' ', body);
			title = title.replace("/", "~");
			quesId = child.get('Id');
			score = child.get('Score');
			views = child.get('ViewCount');

			#get the user id for this post
			userid = child.get('OwnerUserId');

			f = open(folder + title + ".ejs","w") #opens file with name of "test.txt"
			
			#find user information
			userInfoHTML = getUserInfoHTML(userRoot, root, userid, quesId);
			userInfoHTML = re.sub(r'[^\x00-\x7F]+',' ', userInfoHTML);

			#print 'user info ->', userInfoHTML

			#findcomments
			commentStr = findComments(commentRoot, quesId);

			#find answers
			answerStr = findAnswers(root, commentRoot, quesId, userRoot);
			
			content = createContent(title, quesId, body, userInfoHTML, score, views, commentStr, answerStr);

			#print content
			print 'processed ', quesId
			f.write(content);
			f.close();

if __name__ == "__main__":
	main();
