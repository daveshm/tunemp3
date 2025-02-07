### Inference Hosted 

# TuneMP3 - Hosted SVC Model Service

This project provides a hosted version of the [so-vits-svc](https://github.com/svc-develop-team/so-vits-svc) model for voice conversion.

## Architecture

The service is built using:
- Firebase Hosting & Functions for the frontend and API
- Google Cloud Run for model inference
- Google Cloud Storage for artifact storage
- Docker containers for model deployment

## Key Components

### Firebase Setup
- Hosting configured with rewrites for API and inference endpoints
- Functions handling file uploads and processing
- Storage bucket "svc_artifacts_fire" for managing audio files

### Docker Container
- Custom inference container based on Python
- Exposes port 5000 for API access
- Includes necessary ML dependencies and model code

### Cloud Run Integration
- Deployed as a managed service in us-central1
- Handles model inference requests
- Integrated with Firebase hosting through rewrites

## API Endpoints

- `/api/upload` - Handles file uploads to Google Cloud Storage
- `/runcmd` - Triggers model inference
- `/status` - Checks inference status

## Authentication

Uses Google Cloud service accounts for secure access between services.

## Getting Started

1. Deploy the Firebase functions and hosting
2. Build and push the Docker container
3. Deploy to Cloud Run
4. Configure the Firebase rewrites to point to your Cloud Run service

For more details on the implementation, see the source code in the repository.