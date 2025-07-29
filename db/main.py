from fastapi import FastAPI
import sqlite3
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "databasemanager"}))
)
jaeger_exporter = JaegerExporter(
    agent_host_name=os.getenv("JAGER_HOSTNAME", "localhost"),
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(jaeger_exporter))

tracer = trace.get_tracer("databasemanager")

app = FastAPI()
connection = sqlite3.connect('films')


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/')
async def root(id: str):
    with tracer.start_as_current_span("Inserting into database"):
        cursor = connection.cursor()
        try:
            cursor.execute(f'INSERT INTO films VALUES ("{id}")')
        except:
            return 0
        connection.commit()
        return 1


@app.get('/')
async def get_data():
    with tracer.start_as_current_span("getting data from database"):
        cursor = connection.cursor()
        data = cursor.execute(f"SELECT id from films")
        return [j for i in data.fetchall() for j in i]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
