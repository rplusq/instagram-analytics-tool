# Imports to interact with the API

import requests
import json
import datetime

# Functions to interact with the API

def getCreds(one_hour_access_token, client_id, client_secret_key):
    creds = dict()
    creds['access_token'] = one_hour_access_token
    creds['client_id'] = client_id
    creds['client_secret'] = client_secret_key
    creds['graph_domain'] = 'https://graph.facebook.com/'
    creds['graph_version'] = 'v7.0'
    creds['endpoint_base'] = f"{creds['graph_domain']}{creds['graph_version']}/"
    creds['debug'] = False
    
    return creds

def makeApiCall( url, endpointParams, debug = 'no') :
    endpointParams['locale'] = 'en_US'
    data = requests.get(url, endpointParams)
    
    response = dict()
    
    response['url'] = url
    response['endpoint_params'] = endpointParams
    response['endpoint_params_pretty'] = json.dumps( endpointParams, indent = 4 )
    response['json_data'] = json.loads( data.content )
    response['json_data_pretty'] = json.dumps( response['json_data'], indent = 4 )
    
    if (debug) :
        displayApiCallData( response )
    
    return response

def displayApiCallData(response):
    print("\nURL: ")
    print(response['url'])
    print("\nEndpoint Params: ")
    print(response['endpoint_params_pretty'])
    print("\nResponse: ")
    print(response['json_data_pretty'])
    
def debugAccessToken( params ) :
    """ Get info on an access token
    
    API Endpoint:
        https://graph.facebook.com/debug_token?input_token{input-token}&access_token={valid-access-token}
        
        Returns:
            object: data from the endpoint
    """
    
    endpointParams = dict()
    endpointParams['input_token'] = params['access_token']
    endpointParams['access_token'] = params['access_token']
    
    url = f"{params['graph_domain']}/debug_token"
    
    return makeApiCall( url, endpointParams, params['debug'])

def getLongLivedAccessToken( params ):
    """ Get long lived access token
    
    API Endpoint:
        https://graph.facebook.com/{graph-api-version}/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={your-access-token}
        
        
        Returns:
            object: data from the endpoint
    """
    
    endpointParams = dict()
    endpointParams['grant_type'] = 'fb_exchange_token'
    endpointParams['client_id'] = params['client_id']
    endpointParams['client_secret'] = params['client_secret']
    endpointParams['fb_exchange_token'] = params['access_token']
    
    url = f"{params['endpoint_base']}oauth/access_token"
    
    return makeApiCall( url, endpointParams, params['debug'])

def getUserPages( params ):
    """ Get pages for logged user
    
    API Endpoint:
          https://graph.facebook.com/v7.0/me/accounts?access_token={access-token}

        
        
        Returns:
            object: data from the endpoint
    """
    
    endpointParams = dict()
    endpointParams['access_token'] = params['access_token']
    
    url = f"{params['endpoint_base']}me/accounts"
    
    return makeApiCall( url, endpointParams, params['debug'])

def getInstagramBusinessAccounts( params ):
    """ Get pages for logged user
    
    API Endpoint:
          https://graph.facebook.com/v7.0/{page-id}?fields=instagram_business_account&access_token={access-token}

        
        
        Returns:
            object: data from the endpoint
    """
    
    endpointParams = dict()
    endpointParams['access_token'] = params['access_token']
    endpointParams['fields'] = 'instagram_business_account'
    page_id = params['page_id']
    
    url = f"{params['endpoint_base']}{page_id}"
    
    return makeApiCall( url, endpointParams, params['debug'])

def getUserMedia( params, pagingUrl = '' ) :
    """ Get users media

    API Endpoint:
        https://graph.facebook.com/{graph-api-version}/{ig-user-id}/media?fields={fields}&access_token={access-token}
    Returns:
        object: data from the endpoint
    """

    endpointParams = dict() # parameter to send to the endpoint
    endpointParams['fields'] = 'id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username' # fields to get back
    endpointParams['access_token'] = params['access_token'] # access token

    if ( '' == pagingUrl ) : # get first page
        url = params['endpoint_base'] + params['instagram_account_id'] + '/media' # endpoint url
    else : # get specific page
        url = pagingUrl  # endpoint url

    return makeApiCall( url, endpointParams, params['debug'] ) # make the api call

def getMediaInsights( params ) :
    """ Get insights for a specific media id
    
    API Endpoint:
        https://graph.facebook.com/{graph-api-version}/{ig-media-id}/insights?metric={metric}

    Returns:
        object: data from the endpoint

    """
    endpointParams = dict() # parameter to send to the endpoint
    endpointParams['metric'] = params['metric'] # fields to get back
    endpointParams['access_token'] = params['access_token'] # access token

    url = params['endpoint_base'] + params['ig_media_id'] + '/insights' # endpoint url

    return makeApiCall( url, endpointParams, params['debug'] ) # make the api call

def getUserInsights( params ) :
    """ Get insights for a users account
    
    API Endpoint:
        https://graph.facebook.com/{graph-api-version}/{ig-user-id}/insights?metric={metric}&period={period}

    Returns:
        object: data from the endpoint

    """

    endpointParams = dict() # parameter to send to the endpoint
    endpointParams['metric'] = 'follower_count,impressions,profile_views,reach' # fields to get back
    endpointParams['period'] = 'day' # period
    endpointParams['access_token'] = params['access_token'] # access token

    url = params['endpoint_base'] + params['instagram_account_id'] + '/insights' # endpoint url

    return makeApiCall( url, endpointParams, params['debug'] ) # make the api call

def getHashtagInfo( params ) :
    """ Get info on a hashtag

    API Endpoint:
        https://graph.facebook.com/{graph-api-version}/ig_hashtag_search?user_id={user-id}&q={hashtag-name}&fields={fields}
    Returns:
        object: data from the endpoint
    """

    endpointParams = dict() # parameter to send to the endpoint
    endpointParams['user_id'] = params['instagram_account_id'] # user id making request
    endpointParams['q'] = params['hashtag_name'] # hashtag name
    endpointParams['fields'] = 'id,name' # fields to get back
    endpointParams['access_token'] = params['access_token'] # access token

    url = params['endpoint_base'] + 'ig_hashtag_search' # endpoint url

    return makeApiCall( url, endpointParams, params['debug'] ) # make the api call

def getHashtagMedia( params ) :
    """ Get posts for a hashtag
    
    API Endpoints:
        https://graph.facebook.com/{graph-api-version}/{ig-hashtag-id}/top_media?user_id={user-id}&fields={fields}
        https://graph.facebook.com/{graph-api-version}/{ig-hashtag-id}/recent_media?user_id={user-id}&fields={fields}
    Returns:
        object: data from the endpoint
    """

    endpointParams = dict() # parameter to send to the endpoint
    endpointParams['user_id'] = params['instagram_account_id'] # user id making request
    endpointParams['fields'] = 'id,children,caption,comment_count,like_count,media_type,media_url,permalink' # fields to get back
    endpointParams['access_token'] = params['access_token'] # access token

    url = params['endpoint_base'] + params['hashtag_id'] + '/' + params['type'] # endpoint url

    return makeApiCall( url, endpointParams, params['debug'] ) # make the api call

def getRecentlySearchedHashtags( params ) :
    """ Get hashtags a user has recently search for
    
    API Endpoints:
        https://graph.facebook.com/{graph-api-version}/{ig-user-id}/recently_searched_hashtags?fields={fields}
    Returns:
        object: data from the endpoint
    """

    endpointParams = dict() # parameter to send to the endpoint
    endpointParams['fields'] = 'id,name' # fields to get back
    endpointParams['access_token'] = params['access_token'] # access token

    url = params['endpoint_base'] + params['instagram_account_id'] + '/' + 'recently_searched_hashtags' # endpoint url

    return makeApiCall( url, endpointParams, params['debug'] ) # make the api call
