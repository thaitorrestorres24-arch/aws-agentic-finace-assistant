# AWS Agentic Finance Assistant

This is an AI Financial Agent designed for everyday people to help them manage their budget and handle debt. It uses the AWS Strands Decider 2B model and Amazon Bedrock to build a practical assistant for the Brazilian community.

## Purpose
Financial literacy is difficult for everyday people facing high-interest credit card debt or tight monthly budgets. This project allows users to describe their financial problems in plain language. The agent automatically classifies the risk level and provides clear, non-technical advice to help them navigate their situation.

## How It Works
The application uses a dual-model approach:
1. **AWS Strands Decider 2B:** Acts as the logic layer, reading the user's input and categorizing their financial state into Critical, Alert, or Stable.
2. **Amazon Bedrock:** Handles the generative response to deliver practical behavioral steps in Portuguese tailored to the user's category.

## Error Handling
Following the hackathon guidelines for experimental software, the code includes a fallback mechanism. If local hardware latency slows down the system or connection fails, a local rule-based safety mechanism triggers instantly. This ensures the end-user never experiences a frozen interface or a system crash.
