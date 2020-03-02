# -*- coding: utf-8 -*-
import json
import sys
import facebook
import time
from datetime import datetime, timezone
import pandas as pd
from urllib.request import urlopen

token = ''
graph = facebook.GraphAPI(token)

# Get page details
def get_page_details(obj):
    #pages_data = obj.get_object("/FortniteGame")
	pages_data = obj.get_object("/me")
    page_data = pages_data['data']
    page_id = None
    page_name = None
    for elem in page_data:
        page_id = elem['id']
        page_name = elem['name']
    return page_id, page_name

# Get post data
def get_posts_details(page_id):
    posts_conn = graph.get_connections(id=page_id,
                                           connection_name='posts',
                                           fields='created_time')
    posts_data = posts_conn['data']
    post_data_list = []
    for elem in posts_data:
        post_data_dict = {}
        post_data_dict['created_time'] = elem['created_time']
        post_data_dict['id'] = elem['id']
        post_data_list.append(post_data_dict)
    return post_data_list


# driver code to call request on graph API
def request_data_from_url(url):
    try: 
        #open the url
        response = urlopen(url)
        #200 is the success code for http
        if response.getcode() == 200:
            return response.read()
        else:
            return None
    except Exception as e:
        #if we didn't get a success, then print the error adef get_facebook_page_data(page_id, access_token):
        print(e)
        time.sleep(5)
        print('Error for URL: {}'.format(url))
        print("Retrying...")


# Get reaction data
def get_reactions_for_post(post_id, access_token):

    website = "https://graph.facebook.com/v5.0"
    
    location = "/%s" % post_id
    
    #here we ask for the number of reactions of each time associated with this post
    reactions = "/?fields=" \
            "reactions.type(LIKE).limit(0).summary(total_count).as(like)" \
            ",reactions.type(LOVE).limit(0).summary(total_count).as(love)" \
            ",reactions.type(WOW).limit(0).summary(total_count).as(wow)" \
            ",reactions.type(HAHA).limit(0).summary(total_count).as(haha)" \
            ",reactions.type(SAD).limit(0).summary(total_count).as(sad)" \
            ",reactions.type(THANKFUL).limit(0).summary(total_count).as(thankful)" \
            ",reactions.type(ANGRY).limit(0).summary(total_count).as(angry)" \
            ",shares"
    
    authentication = "&access_token=%s" % access_token
    
    request_url = website + location + reactions + authentication

    # retrieve data and store in python dictionary
    data = json.loads(request_data_from_url(request_url))
     
    return data

# Get counts(reaction, likes, shares)
def get_facebook_page_data(page_id, access_token):

    website = "https://graph.facebook.com/v5.0/"
    
    location = "%s/posts/" % page_id 
    
    #the .limit(0).summary(true) is used to get a summarized count of all the ... 
    #...comments and reactions instead of getting each individual one
    fields = "?fields=message,permalink_url,created_time," + \
            "id,comments.limit(0).summary(true),shares.limit(0).summary(true),likes.limit(0).summary(true)," + \
            "reactions.limit(0).summary(true)"
            
    authentication = "&limit=100&access_token=%s" % (access_token)
    
    request_url = website + location + fields + authentication

    #converts facebook's response to a python dictionary to easier manipulate later
    data = json.loads(request_data_from_url(request_url))
    return data

# Driver code for get_facebook_page_data(likes, comments, reactions, shares, engaements counts)
def act_count(fpd_obj):
    count_data_list = []
    for elem in fpd_obj['data']:
        count_data_dict = {}
        if 'id' in elem.keys():
            count_data_dict['id'] = elem['id']
        if 'permalink_url' in elem.keys():
            count_data_dict['permalink_url'] = elem['permalink_url']
        if 'comments' in elem.keys():
            count_data_dict['comments_count_fb'] = int(elem['comments']['summary']['total_count'])
        else:
            count_data_dict['comments_count_fb'] = 0
        if 'likes' in elem.keys():
            count_data_dict['likes_count_fb'] = int(elem['likes']['summary']['total_count'])
        else:
            count_data_dict['likes_count_fb'] = 0
        if 'reactions' in elem.keys():
            count_data_dict['reactions_count_fb'] = int(elem['reactions']['summary']['total_count'])
        else:
            count_data_dict['reactions_count_fb'] = 0
        if 'shares' in elem.keys():
            count_data_dict['shares_count_fb'] = int(elem['shares']['count'])
        else:
            count_data_dict['shares_count_fb'] = 0
        
        count_data_dict['engagements_count_fb'] = count_data_dict['comments_count_fb']+\
                                                    count_data_dict['reactions_count_fb']+count_data_dict['shares_count_fb']
        count_data_list.append(count_data_dict)
    return count_data_list


# Get post type and post message associated
def get_post_type(page_id):
    query_string = 'posts?limit={0}'.format(100)
    posts_data1 = graph.get_connections(page_id, query_string)
    dat_1 = posts_data1['data']
    post_typ_list = []
    for val in dat_1:
        post_typ_dict = {}
        post_typ_dict['id'] = val['id']
        post_typ_dict['message'] = ''
        post_typ_dict['story'] = ''
        post_typ_dict['type'] = 'NA'
        if 'message' in val.keys():
            post_typ_dict['message'] = val['message']
            if val['message'].startswith('http'):
                post_typ_dict['type'] = 'link'
            else:
                gpp_data = get_page_post_det(val['id'], token)
                st_type = gpp_data['status_type']
                if st_type.split('_')[-1] == 'photos':
                    post_typ_dict['type'] = 'photo'
                elif st_type.split('_')[-1] == 'video':
                    post_typ_dict['type'] = 'video'
                else:
                    post_typ_dict['type'] = 'story'
            
        elif 'story' in val.keys():
            post_typ_dict['story'] = val['story']
            if val['story'].startswith('http'):
                post_typ_dict['type'] = 'link'
            else:
                gpp_data = get_page_post_det(val['id'], token)
                st_type = gpp_data['status_type']
                if st_type.split('_')[-1] == 'photos':
                    post_typ_dict['type'] = 'photo'
                elif st_type.split('_')[-1] == 'video':
                    post_typ_dict['type'] = 'video'
                else:
                    post_typ_dict['type'] = 'story'
        else:
            gpp_data = get_page_post_det(val['id'], token)
            st_type = gpp_data['status_type']
            if st_type.split('_')[-1] == 'photos':
                post_typ_dict['type'] = 'photo'
            elif st_type.split('_')[-1] == 'video':
                post_typ_dict['type'] = 'video'
            else:
                post_typ_dict['type'] = 'story'
        post_typ_list.append(post_typ_dict)
    return post_typ_list


# get comments and comment replies data
def get_comment_data(comm_id):
    
    website = "https://graph.facebook.com/v5.0/"
    
    location = "{}".format(comm_id)
    fields = "?fields=message,permalink_url,created_time," + \
            "id,comments.limit(0).summary(true),likes.limit(0).summary(true)," + \
            "reactions.limit(0).summary(true)"
            
    authentication = "&access_token=%s" % (token)
    
    request_url = website + location + fields + authentication
    
    #converts facebook's response to a python dictionary to easier manipulate later
    data = json.loads(request_data_from_url(request_url))
    
    return data


# Get full picture, status_type
def get_page_post_det(page_post, token):

    website = "https://graph.facebook.com/v5.0/"
    location = "{}".format(page_post)
    fields = "?fields=id,created_time,from," + \
            "full_picture," + \
            "status_type"#import re

    authentication = "&limit=100&access_token=%s" % (token)
    ref = website + location + fields + authentication
    data = json.loads(request_data_from_url(ref))
    return data


# Get picture link
def get_post_det(post_id, token):

    website = "https://graph.facebook.com/v5.0/"
    location = "{}".format(post_id)
    fields = "?fields=id,picture"

    authentication = "&limit=100&access_token=%s" % (token)
    ref = website + location + fields + authentication
    data = json.loads(request_data_from_url(ref))
    return data


# Get total comment on posts(comments+replies)
def get_post_comm_det(post_id, token):

    website = "https://graph.facebook.com/v5.0/"
    location = "{}/comments?summary=1&filter=stream".format(post_id)
    authentication = "&access_token=%s" % (token)
    ref = website + location + authentication
    data = json.loads(request_data_from_url(ref))
    return data

# Get link and link domain data
def get_link_data(post_id):
    stt = '{}/attachments?'.format(post_id)
    website = "https://graph.facebook.com/"
    authentication = "access_token=%s" % (token)
    ref = website + stt + authentication
    data = json.loads(request_data_from_url(ref))
    return data

# Create excel file 
def create_excel(data_list, page_id,exl_name):
    data_df = pd.DataFrame(data_list)
    sht_name = str('page_'+str(page_id)+'_'+str(datetime.now()).replace(':', '%').split('.')[0].replace('-','_')).split(' ')[0]
    writer = pd.ExcelWriter(str(exl_name), engine='xlsxwriter',options={'strings_to_urls': False})
    data_df.to_excel(writer, sheet_name=sht_name, index=False)
    writer.close()



if __name__ == '__main__':
    page_id, page_name = get_page_details(graph)
    if page_id is None:
        sys.exit('Page details Not found!')
    post_data_list = get_posts_details(page_id)
    gpd_data = get_facebook_page_data(page_id, token)
    count_data = act_count(gpd_data)
    gpt_data = get_post_type(page_id)
    fb_data_list = []
    for elem in gpd_data['data']:
        fb_data_dict = {}
        # Get post message and type
        elemey = (x for x in gpt_data if x['id'] == elem['id'])
        for ey in elemey:
            if ey['id'] == elem['id']:
                fb_data_dict['type'] = ey['type']
                if ey['message']:
                    fb_data_dict['post_message'] = ey['message']
                elif ey['story']:
                    fb_data_dict['post_message'] = ey['story']
                else:
                    fb_data_dict['post_message'] = ''
        fb_data_dict['by'] = 'post_page_'+str(elem['id'].split('_')[0])
        fb_data_dict['post_id'] = elem['id']
        gpd_pic_dat = get_post_det(elem['id'], token)  
        if 'picture' in gpd_pic_dat.keys():
            fb_data_dict['picture'] = gpd_pic_dat['picture']
        else:
            fb_data_dict['picture'] = ''
        gpp_data = get_page_post_det(elem['id'], token)
        if 'full_picture' in gpp_data.keys():
            fb_data_dict['full_picture'] = gpp_data['full_picture']
        # Get link and link domain
        gld_data = get_link_data(elem['id'])
        fb_data_dict['link'] = ''
        for lin in gld_data['data']:
            if 'source' in lin['media'].keys():
                fb_data_dict['link'] = lin['media']['source']
            else:
                fb_data_dict['link'] = lin['target']['url']
        if fb_data_dict['link'] != '':
            fb_data_dict['link_domain'] = fb_data_dict['link'].split('/')[2]
        else:
            fb_data_dict['link_domain'] = ''
        # Post published date
        fb_data_dict['post_published'] = elem['created_time']
        # create unix timestamp
        st = elem['created_time'].split('-')
        dte = datetime(int(st[0]), int(st[1]), int(st[2][:2]))
        timestamp = dte.replace(tzinfo=timezone.utc).timestamp()
        fb_data_dict['post_published_unix'] = int(timestamp)
        # Create Sql timestamp
        ste = elem['created_time'].replace('T', ' ').replace('-', '/').split('+')[0].split(' ')
        ste[0] = ste[0][2:]
        ste[1] = str(int(ste[1].split(':')[0])+12)+ste[1][2:]
        fb_data_dict['post_published_sql'] = ' '.join(ste)
        
        elemex  = (x for x in count_data if x['id'] == elem['id'])
        for ex in elemex:
            if ex['id'] == elem['id']:
                fb_data_dict['post_link'] = ex['permalink_url']
                fb_data_dict['likes_count_fb'] = ex['likes_count_fb']
                fb_data_dict['comments_count_fb'] = ex['comments_count_fb']
                fb_data_dict['reactions_count_fb'] = ex['reactions_count_fb']
                fb_data_dict['shares_count_fb'] = ex['shares_count_fb']
                fb_data_dict['engagements_count_fb'] = ex['engagements_count_fb']
        com_retrieved = get_post_comm_det(elem['id'], token)
        fb_data_dict['comments_retrieved'] = com_retrieved['summary']['total_count']
        comment_base_count = 0
        comments_data = graph.get_connections(id=elem['id'], connection_name='comments')
        for comm_id in comments_data['data']:
            get_cdata = get_comment_data(comm_id['id'])
            comment_base_count += 1
        fb_data_dict['comments_base'] = comment_base_count
        fb_data_dict['comments_replies'] = int(fb_data_dict['comments_retrieved']) - int(comment_base_count)
        count_comm_likes = 0
        for elem_c in com_retrieved['data']:
            gcd = get_comment_data(elem_c['id'])
            count_comm_likes += gcd['likes']['summary']['total_count']
        fb_data_dict['comment_likes_count'] = count_comm_likes
        reactn_data = get_reactions_for_post(elem['id'], token)
        fb_data_dict['rea_LOVE'] = reactn_data['love']['summary']['total_count']
        fb_data_dict['rea_WOW'] = reactn_data['wow']['summary']['total_count']
        fb_data_dict['rea_HAHA'] = reactn_data['haha']['summary']['total_count']
        fb_data_dict['rea_SAD'] = reactn_data['sad']['summary']['total_count']
        fb_data_dict['rea_THANKFUL'] = reactn_data['thankful']['summary']['total_count']
        fb_data_dict['rea_ANGRY'] = reactn_data['angry']['summary']['total_count']
        fb_data_list.append(fb_data_dict)
    
    exl_name = page_name+"FB Full Stats last 100"+".xlsx"
    create_excel(fb_data_list, page_id, exl_name)