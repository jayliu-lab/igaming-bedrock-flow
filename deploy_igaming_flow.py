#!/usr/bin/env python3
import boto3
import json
import sys

def get_account_id():
    """Get AWS account ID"""
    sts = boto3.client('sts')
    return sts.get_caller_identity()['Account']

def deploy_flow():
    """Deploy the iGaming player inquiry flow"""
    
    # Initialize Bedrock client
    bedrock = boto3.client('bedrock-agent', region_name='us-east-1')
    
    # Get account ID and update ARN
    account_id = get_account_id()
    
    # Load flow definition
    with open('igaming_player_inquiry_flow.json', 'r') as f:
        flow_def = json.load(f)
    
    # Update agent ARN with actual account ID
    for node in flow_def['definition']['nodes']:
        if node['type'] == 'Agent':
            current_arn = node['configuration']['agent']['agentAliasArn']
            node['configuration']['agent']['agentAliasArn'] = current_arn.replace('ACCOUNT_ID', account_id)
    
    try:
        # Create the flow
        response = bedrock.create_flow(
            name=flow_def['name'],
            description=flow_def['description'],
            executionRoleArn=f'arn:aws:iam::{account_id}:role/AmazonBedrockExecutionRoleForFlows_*',
            definition=flow_def['definition'],
            tags=flow_def['tags']
        )
        
        flow_id = response['id']
        print(f"✅ Flow created successfully!")
        print(f"Flow ID: {flow_id}")
        print(f"Flow ARN: {response['arn']}")
        
        # Prepare the flow
        prepare_response = bedrock.prepare_flow(flowIdentifier=flow_id)
        print(f"✅ Flow preparation initiated")
        
        return flow_id
        
    except Exception as e:
        print(f"❌ Error creating flow: {str(e)}")
        return None

def test_flow(flow_id, test_query="I can't withdraw my winnings"):
    """Test the deployed flow"""
    
    bedrock_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1')
    
    try:
        response = bedrock_runtime.invoke_flow(
            flowIdentifier=flow_id,
            flowAliasIdentifier='TSTALIASID',
            inputs=[
                {
                    'content': {
                        'document': test_query
                    },
                    'nodeName': 'PlayerInputNode',
                    'nodeOutputName': 'document'
                }
            ]
        )
        
        print(f"\n🧪 Test Query: {test_query}")
        print(f"📋 Response: {response}")
        
    except Exception as e:
        print(f"❌ Error testing flow: {str(e)}")

if __name__ == "__main__":
    print("🚀 Deploying iGaming Player Inquiry Flow...")
    
    flow_id = deploy_flow()
    
    if flow_id and len(sys.argv) > 1 and sys.argv[1] == '--test':
        print("\n⏳ Waiting for flow to be ready...")
        import time
        time.sleep(10)  # Wait for preparation
        test_flow(flow_id)