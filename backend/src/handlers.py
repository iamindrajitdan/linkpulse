import json
import logging
from services import LinkService
from repository import DynamoRepository

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def create_response(status_code: int, body: dict):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body)
    }

def shorten_handler(event, context):
    try:
        body = json.loads(event['body'])
        url = body.get('url')
        ttl_hours = body.get('ttl_hours', 24)
        
        if not url:
            return create_response(400, {'error': 'URL is required'})
        
        repository = DynamoRepository()
        service = LinkService(repository)
        link_data = service.create_short_link(url, ttl_hours)
        
        return create_response(200, {
            'slug': link_data.slug,
            'short_url': f"https://your-domain.com/u/{link_data.slug}",
            'original_url': link_data.original_url,
            'expires_at': link_data.expires_at
        })
        
    except ValueError as e:
        return create_response(400, {'error': str(e)})
    except Exception as e:
        logger.error(f"Error in shorten_handler: {str(e)}")
        return create_response(500, {'error': 'Internal server error'})

def redirect_handler(event, context):
    try:
        slug = event['pathParameters']['slug']
        ip = event['requestContext']['identity']['sourceIp']
        user_agent = event['headers'].get('User-Agent', 'Unknown')
        
        repository = DynamoRepository()
        service = LinkService(repository)
        redirect_url = service.get_redirect_url(slug, ip, user_agent)
        
        if not redirect_url:
            return create_response(404, {'error': 'Link not found or expired'})
        
        return {
            'statusCode': 302,
            'headers': {
                'Location': redirect_url,
                'Access-Control-Allow-Origin': '*'
            }
        }
        
    except Exception as e:
        logger.error(f"Error in redirect_handler: {str(e)}")
        return create_response(500, {'error': 'Internal server error'})

def analytics_handler(event, context):
    try:
        slug = event['pathParameters']['slug']
        
        repository = DynamoRepository()
        service = LinkService(repository)
        analytics = service.get_analytics(slug)
        
        if not analytics:
            return create_response(404, {'error': 'Link not found'})
        
        return create_response(200, {
            'total_clicks': analytics.total_clicks,
            'first_click': analytics.first_click,
            'last_click': analytics.last_click,
            'click_logs': [
                {
                    'timestamp': log.timestamp,
                    'ip': log.ip,
                    'country': log.country,
                    'user_agent': log.user_agent
                } for log in analytics.click_logs
            ]
        })
        
    except Exception as e:
        logger.error(f"Error in analytics_handler: {str(e)}")
        return create_response(500, {'error': 'Internal server error'})