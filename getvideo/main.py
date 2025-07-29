from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import random
import uvicorn
import os
from googleapiclient.discovery import build
from prometheus_fastapi_instrumentator import Instrumentator
import json
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

app = FastAPI()

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "getvideo"}))
)
jaeger_exporter = JaegerExporter(
    agent_host_name=os.getenv("JAGER_HOSTNAME", "localhost"),
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

tracer = trace.get_tracer("getvideo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

api_key = 'your_api_key'
youtube = build('youtube', 'v3', developerKey=api_key)
@app.get("/")
async def root():
    with tracer.start_as_current_span("Getting random video"):
        request = youtube.videos().list(
            part="snippet",
            chart="mostPopular",
            regionCode="RU",
            maxResults=100
        )
        response = request.execute()

        random_video = random.choice(response.get('items', []))

        if random_video:
            return {'snippet': random_video['snippet'], 'id' :random_video['id']}
        else:
            return {"message": "No videos found"}

@app.get("/list/")
async def get_list(q: list | None = Query()):
    with tracer.start_as_current_span("Getting list of videos"):
        video_list = []
        for video_id in q:
            request = youtube.videos().list(
                part="snippet",
                id=video_id
            )
            response = request.execute()
            video_list.append({'snippet':response['items'][0]['snippet'], 'id':response['items'][0]['id']})
        return video_list


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))

