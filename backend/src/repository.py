import boto3
import json
import os
from typing import Optional
from boto3.dynamodb.conditions import Key
from models import LinkData, ClickLog, Analytics

class DynamoRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(os.environ['TABLE_NAME'])

    def save_link(self, link_data: LinkData):
        item = {
            'slug': link_data.slug,
            'original_url': link_data.original_url,
            'created_at': link_data.created_at,
            'click_count': link_data.click_count,
            'click_logs': []
        }
        if link_data.expires_at:
            item['expires_at'] = link_data.expires_at
        
        self.table.put_item(Item=item)

    def get_link(self, slug: str) -> Optional[LinkData]:
        try:
            response = self.table.get_item(Key={'slug': slug})
            if 'Item' not in response:
                return None
            
            item = response['Item']
            return LinkData(
                slug=item['slug'],
                original_url=item['original_url'],
                created_at=item['created_at'],
                expires_at=item.get('expires_at'),
                click_count=item.get('click_count', 0)
            )
        except:
            return None

    def log_click(self, slug: str, click_log: ClickLog):
        self.table.update_item(
            Key={'slug': slug},
            UpdateExpression='ADD click_count :inc SET click_logs = list_append(if_not_exists(click_logs, :empty_list), :click)',
            ExpressionAttributeValues={
                ':inc': 1,
                ':empty_list': [],
                ':click': [{
                    'timestamp': click_log.timestamp,
                    'ip': click_log.ip,
                    'user_agent': click_log.user_agent,
                    'country': click_log.country
                }]
            }
        )

    def get_analytics(self, slug: str) -> Optional[Analytics]:
        try:
            response = self.table.get_item(Key={'slug': slug})
            if 'Item' not in response:
                return None
            
            item = response['Item']
            click_logs = [
                ClickLog(
                    timestamp=log['timestamp'],
                    ip=log['ip'],
                    user_agent=log['user_agent'],
                    country=log['country']
                ) for log in item.get('click_logs', [])
            ]
            
            timestamps = [log.timestamp for log in click_logs]
            return Analytics(
                total_clicks=item.get('click_count', 0),
                first_click=min(timestamps) if timestamps else None,
                last_click=max(timestamps) if timestamps else None,
                click_logs=click_logs
            )
        except:
            return None