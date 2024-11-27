from spleeter_service import SpleeterService

service = SpleeterService()
result = service.process_audio('test.wav')
print(f"Processing {'successful' if result else 'failed'}")
