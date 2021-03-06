import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
import re
from random import randrange
from random import *
from redis_helper import load_obj_from_redis
from redis_helper import save_obj_in_redis
from misc import *
import redis
import json
from redis_helper import load_obj_from_redis
from redis_helper import save_obj_in_redis

def get_tags_array_from_tree(tag_tree):
	tags = []
	root = tag_tree.getroot();
	for child in root:
		tag = child.get('TagName');
		if tag not in tags:
			tags.append(tag);
	return tags


def get_random_tags(tag_array):
	#choose 3 random tags
	chosen_tags = []
	while True:
		random_index = randrange(0,len(tag_array))
		if tag_array[random_index] not in chosen_tags:
			chosen_tags.append(tag_array[random_index]);
			if len(chosen_tags) ==3:
				break;
	return chosen_tags

def get_post_for_tag(tag, tag_post_obj):

	tag_questions = tag_post_obj[tag]['questions']
	random_index = randrange(0,len(tag_questions))
	return tag_post_obj[tag]['questions'][random_index]
	

def get_activity_for_user(activity_count, tags, userId, tag_post_obj, post_store):
	act_obj = []
	#print 'userid -->', userId
	#print 'tags-->', tags
	for i in range(activity_count):
		random_number = random()
		if random_number>=0 and random_number <0.5:
			#pick tag 1
			#print 'tag 1'
			
			post = get_post_for_tag(tags[0], tag_post_obj);
		elif random_number>=0.5 and random_number<0.75:
			#pick tag 2
			#print 'tag 2'
			
			if len(tags) > 1:
				post = get_post_for_tag(tags[1], tag_post_obj);
			else:
				post = get_post_for_tag(tags[0], tag_post_obj);
		elif random_number>=0.75 and random_number<1:
			#pick tag 3
			#print 'tag 3';
			if len(tags) > 2:
				post = get_post_for_tag(tags[2], tag_post_obj);
			elif len(tags) >1:
				post = get_post_for_tag(tags[1], tag_post_obj);
			else:
				post = get_post_for_tag(tags[0], tag_post_obj);
		#print post;
		act_obj.append(post);
		#get answers and comments for this post and append that to user activity as well
		postid = post
		#print 'post id-->', postid;
		postanswers = post_store[postid]['answers'];
		#print 'postanswers-->', postanswers
		for postanswer in postanswers:
			act_obj.append(postanswer)

	#print act_obj
	return act_obj;


def get_tags_for_user(userId, user_tag_store):
	tags = user_tag_store[userId];
	return tags

def create_browsing_pattern_for_not_active_users(no_activity_users, tag_array, tag_post_obj, post_store):
	non_active_users_activity_obj = {}
	for userId in no_activity_users:
		#get upvotes, downvotes, reputation and about me section
		#userId = child.get('Id');
		activity_count = randrange(10,20)
		tags = get_random_tags(tag_array)
		#print tags
		act_obj = get_activity_for_user(activity_count, tags, userId, tag_post_obj, post_store);
		non_active_users_activity_obj[userId] = act_obj;

	return non_active_users_activity_obj;

def create_browsing_pattern_for_active_users(final_user_list, tag_post_obj, user_tag_store, post_store, user_activity_obj):
	for userId in final_user_list:

		if userId is not None:
			activity_count = randrange(30,40)
			tags = get_tags_for_user(userId, user_tag_store)

			act_obj = get_activity_for_user(activity_count, tags, userId, tag_post_obj, post_store);

			if userId in user_activity_obj:
				user_activity_obj[userId] = user_activity_obj[userId] + list(set(act_obj) - set(user_activity_obj[userId]))	
			else:
				user_activity_obj[userId] = act_obj

	return user_activity_obj;

def main():

	post_tree = ET.parse('../data/robotics.stackexchange.com/Posts.xml');
	comment_tree = ET.parse('../data/robotics.stackexchange.com/Comments.xml');
	user_tree = ET.parse('../data/robotics.stackexchange.com/Users.xml');
	tag_tree = ET.parse('../data/robotics.stackexchange.com/Tags.xml');

	all_users = get_all_users(user_tree);

	post_users = find_user_list_from_posts(post_tree);
	comment_users = find_user_list_from_comments(comment_tree);

	final_user_list = post_users + list(set(comment_users) - set(post_users));

	print len(all_users);
	print len(post_users);
	print len(comment_users);
	print len(final_user_list);

	no_activity_users = list(set(all_users) - set(final_user_list));
	print len(no_activity_users);

	tag_post_obj = load_obj_from_redis('tag_post_store');

	#retrieve the saved user-tag structure
	user_tag_store = load_obj_from_redis('user_tag_store');
	print user_tag_store['21']

	#retrieve the saved post structure
	post_store = load_obj_from_redis('post_store');
	
	tags_arr = get_tags_array_from_tree(tag_tree);
	user_activity_obj = create_browsing_pattern_for_not_active_users(no_activity_users, tags_arr, tag_post_obj, post_store);
	print len(user_activity_obj)
	user_activity_obj = create_browsing_pattern_for_active_users(final_user_list, tag_post_obj, user_tag_store, post_store, user_activity_obj);
	print len(user_activity_obj)
	print 'length of the user activity table -->', len(user_activity_obj)

	#update user-tag-table
	
	#print 'saving simulated activity data structure to redis'
	tfidf_obj = load_obj_from_redis('tfidf_obj');
	save_obj_in_redis('user_activity_obj', user_activity_obj);
	user_keywords_store = {};

	for userid in user_activity_obj:
		if userid is not None:
			posts = user_activity_obj[userid]
			#print posts
			for post in posts:
				if post is not None and post in tfidf_obj:
					#print 'post present'
					keywords = tfidf_obj[post]
					#print keywords

					if userid not in user_keywords_store:
						#print 'creating new entry'
						user_keywords_store[userid] = keywords[:20]
					elif userid in user_keywords_store:
						if user_keywords_store[userid] is None:
							user_keywords_store[userid] = keywords[:20];
						else:
							user_keywords_store[userid] = user_keywords_store[userid].append(keywords[:20]);

	#print 'user keyword store-->', str(user_keywords_store)
	for user in user_keywords_store:
		print user
		print user_keywords_store[user]
	print len(user_keywords_store);
	save_obj_in_redis('user_keywords_store', user_keywords_store )
	print 'user keywords store saved...';


if __name__ == "__main__":
	main();