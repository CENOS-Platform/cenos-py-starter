from src.cenos_adapter import load_cenos_api
api = load_cenos_api()
print(f"CENOS API import succeeded: {api.__name__}")
