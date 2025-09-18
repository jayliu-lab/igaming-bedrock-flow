# iGaming Player Inquiry Flow

AWS Bedrock Flow for handling iGaming player inquiries with AI-powered classification and routing.

## Overview

This flow processes player inquiries and routes them to appropriate specialized agents:
- **Classification Agent**: Routes queries to FAQ or Payment agents
- **FAQ Agent**: Handles general questions using Knowledge Base
- **Payment Agent**: Processes payment/withdrawal issues via Lambda

## Flow Architecture

```
Player Input → Classification Agent → Specialized Response
```

## Files

- `flow_definition.json` - Bedrock Flow configuration
- `deploy_igaming_flow.py` - Python deployment script
- `invoke-agent-policy.json` - IAM permissions

## Deployment

### Using AWS CLI
```bash
# Create execution role
aws iam create-role --role-name BedrockFlowExecutionRole --assume-role-policy-document file://trust-policy.json
aws iam attach-role-policy --role-name BedrockFlowExecutionRole --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

# Deploy flow
aws bedrock-agent create-flow \
  --name "igaming-player-inquiry-flow" \
  --execution-role-arn "arn:aws:iam::ACCOUNT_ID:role/BedrockFlowExecutionRole" \
  --definition file://flow_definition.json

# Prepare flow
aws bedrock-agent prepare-flow --flow-identifier FLOW_ID
```

### Using Python
```bash
python deploy_igaming_flow.py
```

## Testing

### AWS Console
1. Go to Bedrock → Flows
2. Select "igaming-player-inquiry-flow"
3. Click **"Create execution"**
4. Enter test query: "I cannot withdraw my winnings"

### AWS CLI
```bash
aws bedrock-agent-runtime start-flow-execution \
  --flow-identifier FLOW_ID \
  --flow-alias-identifier TSTALIASID \
  --inputs '[{"content":{"document":"I cannot withdraw my winnings"},"nodeName":"PlayerInputNode","nodeOutputName":"document"}]'
```

## Agents Used

- **iGaming-Problem-Classification-Agent** (OBFMXNRLA9) - Supervisor
- **iGaming-FAQ-Agent** (E2CCADGSKL) - FAQ handling
- **iGaming-Payment-Agent** (4EMU34V9JY) - Payment processing

## Requirements

- AWS Bedrock access
- Existing iGaming agents configured
- IAM permissions for agent invocation