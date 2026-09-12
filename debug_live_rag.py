import os
from dotenv import load_dotenv

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(PROJECT_ROOT, '.env'))
print('KEY_LOADED', bool(os.getenv('GROQ_API_KEY')))

from src.rag_pipeline import RAGPipeline

pipe = RAGPipeline()
pipe.process_pdf('data')

for q in ['What is supervised learning?', 'What is machine learning?']:
    print('\n' + '=' * 120)
    print('QUESTION:', q)
    print('=' * 120)
    result = pipe.ask(q)
    print('\nFINAL_RETURN_VALUE:', result)
    print('=' * 120)
