# -*- coding: utf-8 -*-

import requests
import json
import pandas as pd
from datetime import datetime


API_ENDPOINT = 'https://discordapp.com/api/v6'

baseUrl = "https://discordapp.com/api/v6"
clientid = ''
clientsecret = ''
# If we want to get data from all channels inside a guild provide guild_id and set CHANNEL_ID = ''
guild_id = ''
# To get data from a Channel data provide channel id below
CHANNEL_ID = ''
# bot token
token = ''



def getHeaders():
    return {
        "Authorization" : "{} {}".format("Bot", token),
    } 

def getRequest(endpoint, headers):
    asJson = True
    url = "{}/{}".format(baseUrl, endpoint)
    req = requests.get(url, headers = headers)
    if asJson:
        return json.loads(req.text)
    else:
        return req.text
    
def get_user_details(headers):
    endpoint_1 = "users/@me" # works
    user_details = getRequest(endpoint_1,headers)
    return user_details

def get_guild_details(headers):
    endpoint_2 = "users/@me/guilds"
    guilds_details = getRequest(endpoint_2,headers)
    return guilds_details

def get_connection_details(headers):
    endpoint_3 = 'users/@me/connections'
    connection_details = getRequest(endpoint_3,headers)
    return connection_details

def get_channel_details(channel_id,headers):
    endpoint_4 = 'channels/{}'.format(channel_id)
    channel_details = getRequest(endpoint_4,headers)
    return channel_details
    
def get_channel_messages(channel_id, headers):
    endpoint_5 = 'channels/{}/messages?limit=100'.format(channel_id)
    channel_messages = getRequest(endpoint_5,headers)
    return channel_messages

def get_guild_chnnls(guild_id, headers):
    endpoint_6 = '/guilds/{}/channels'.format(guild_id)
    guild_details = getRequest(endpoint_6,headers)
    return guild_details

def create_excel(data_list, exl_name):
    data_df = pd.DataFrame(data_list)
    sht_name = str(datetime.now()).replace(':', '%').split('.')[0]
    writer = pd.ExcelWriter(str(exl_name), engine='xlsxwriter',options={'strings_to_urls': False})
    data_df.to_excel(writer, sheet_name=sht_name, index=False)
    writer.close()

def format_message_data(chnnl_data,message_data):    
    channel_message_list = []
    for msg in message_data:
        channel_message_dict = {}
        channel_message_dict['channel-id'] = chnnl_data['id']
        channel_message_dict['channel-last_message_id'] = chnnl_data['last_message_id']
        channel_message_dict['channel-type'] = chnnl_data['type']
        channel_message_dict['channel-name'] = chnnl_data['name']
        channel_message_dict['channel-position'] = chnnl_data['position']
        channel_message_dict['channel-parent_id'] = chnnl_data['parent_id']
        channel_message_dict['channel-topic'] = chnnl_data['topic']
        channel_message_dict['channel-guild_id'] = chnnl_data['guild_id']
        for elem in chnnl_data['permission_overwrites']:
            channel_message_dict['channel-permission-id'] = elem['id']
            channel_message_dict['channel-permission-type'] = elem['type']
            channel_message_dict['channel-permission-allow'] = elem['allow']
            channel_message_dict['channel-permission-deny'] = elem['deny']
        channel_message_dict['channel-nsfw'] = chnnl_data['nsfw']
        channel_message_dict['Message-id'] = msg['id']
        channel_message_dict['Message-type'] = msg['type']
        channel_message_dict['Message-content'] = msg['content']
        channel_message_dict['Message-author-id'] = msg['author']['id']
        channel_message_dict['Message-author-username'] = msg['author']['username']
        channel_message_dict['Message-author-avatar'] = msg['author']['avatar']
        channel_message_dict['Message-author-discriminator'] = msg['author']['discriminator']
        # get attachment data
        if 'attachments' in msg.keys():
            for att in msg['attachments']:
                channel_message_dict['Message-attachments-id'] = att['id']
                channel_message_dict['Message-attachments-filename'] = att['filename']
                channel_message_dict['Message-attachments-size'] = att['size']
                channel_message_dict['Message-attachments-url'] = att['url']
                channel_message_dict['Message-attachments-proxy_url'] = att['proxy_url']
        else:
            channel_message_dict['Message-attachments-id'] = ''
            channel_message_dict['Message-attachments-filename'] = ''
            channel_message_dict['Message-attachments-size'] = ''
            channel_message_dict['Message-attachments-url'] = ''
            channel_message_dict['Message-attachments-proxy_url'] = ''
        
        for embed in msg['embeds']:
            if 'type' in embed.keys():
                channel_message_dict['Message-embed-type'] = embed['type']
            else:
                channel_message_dict['Message-embed-type'] = ''
            if 'url' in embed.keys():
                channel_message_dict['Message-embed-url'] = embed['url']
            else:
                channel_message_dict['Message-embed-url'] = ''
            if 'title' in embed.keys():
                channel_message_dict['Message-embed-title'] = embed['title']
            else:
                channel_message_dict['Message-embed-title'] = ''
            if 'description' in embed.keys():
                channel_message_dict['Message-embed-description'] = embed['description']
            else:
                channel_message_dict['Message-embed-description'] = ''
            if 'provider' in embed.keys():
                channel_message_dict['Message-embed-provider-name'] = embed['provider']['name']
                channel_message_dict['Message-embed-provider-url'] = embed['provider']['url']
            else:
                channel_message_dict['Message-embed-provider-name'] = ''
                channel_message_dict['Message-embed-provider-url'] = ''
            if 'thumbnail' in embed.keys():
                channel_message_dict['Message-embed-thumbnail-url'] = embed['thumbnail']['url']
                channel_message_dict['Message-embed-thumbnail-proxy_url'] = embed['thumbnail']['proxy_url']
            else:
                channel_message_dict['Message-embed-thumbnail-url'] = ''
                channel_message_dict['Message-embed-thumbnail-proxy_url'] = ''
        # Get mentions list details(id, username, discriminators)
        mention_ids = ''
        mentions_usernames = ''
        mentions_discriminators = ''
        if len(msg['mentions']) != 0:
            for ment in msg['mentions']:
                mention_ids = ment['id'].join(' ,')
                mentions_usernames = ment['username'].join(' ,')
                mentions_discriminators = ment['discriminator'].join(' ,')
            channel_message_dict['Message-mentions-id'] = mention_ids
            channel_message_dict['Message-mentions-usernames'] = mentions_usernames
            channel_message_dict['Message-mentions-discriminators'] = mentions_discriminators
        else:
            channel_message_dict['Message-mentions-id'] = mention_ids
            channel_message_dict['Message-mentions-usernames'] = mentions_usernames
            channel_message_dict['Message-mentions-discriminators'] = mentions_discriminators
        if len(msg['mention_roles']) != 0:
            channel_message_dict['Message-mention_roles'] = msg['mention_roles']
        else:
            channel_message_dict['Message-mention_roles'] = ''
        channel_message_dict['Message-pinned'] = msg['pinned']
        channel_message_dict['Message-mention_everyone'] = msg['mention_everyone']
        channel_message_dict['Message-tts'] = msg['tts']
        channel_message_dict['Message-timestamp'] = msg['timestamp']
        channel_message_dict['Message-edited_timestamp'] = msg['edited_timestamp']
        channel_message_dict['Message-flags'] = msg['flags']
        if 'reactions' in msg.keys():
            emoji_names = ''
            emoji_ids = ''
            reaction_count = 0 
            for react in msg['reactions']:
                if react['emoji']['id'] is not None:
                    emoji_ids = react['emoji']['id'].join(' ,')
                if react['emoji']['name'] is not None:
                    emoji_names = react['emoji']['name'].join(' ,')
                if 'animated' in react['emoji'].keys():
                    channel_message_dict['Message-reactions-emoji-animated'] = react['emoji']['animated']
                else:
                    channel_message_dict['Message-reactions-emoji-animated'] = False
                reaction_count += react['count']
                channel_message_dict['Message-reactions-emoji-me'] = react['me']
            channel_message_dict['Message-reactions-emoji-ids'] = emoji_ids
            channel_message_dict['Message-reactions-emoji-names'] = emoji_names
            channel_message_dict['Message-reactions-count'] = reaction_count
        else:
            channel_message_dict['Message-reactions-emoji-id'] = ''
            channel_message_dict['Message-reactions-emoji-name'] = ''
            channel_message_dict['Message-reactions-emoji-animated'] = ''
            channel_message_dict['Message-reactions-emoji-count'] = ''
            channel_message_dict['Message-reactions-emoji-me'] = ''
        channel_message_list.append(channel_message_dict)
        
    return channel_message_list

    
    
if __name__ == '__main__':
    headers = getHeaders()
    guild_chnnls = []
    if CHANNEL_ID == '':
        guild_chnnl_details = get_guild_chnnls(guild_id, headers)
        for chhn in guild_chnnl_details:
            guild_chnnls.append(chhn['id'])
    else:
        guild_chnnls.append(CHANNEL_ID)
    # Get channel data
    for channel_id in guild_chnnls:
        chnnl_data = get_channel_details(channel_id,headers)
        if 'name' and 'id' in chnnl_data.keys():
            # Get messages from channel
            message_data = get_channel_messages(channel_id, headers)
            if len(message_data) != 0:            
                data_list = format_message_data(chnnl_data,message_data)
                print('\nNumber of messages fetched: {}'.format(len(data_list)))
                exl_name = 'dis_chnn_'+str(chnnl_data['name'])+'_'+str(chnnl_data['id'])+'.xlsx'
                # create channel_message_data excel file
                create_excel(data_list, exl_name)  
    
    
    
    
    
    

