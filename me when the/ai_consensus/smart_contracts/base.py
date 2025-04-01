import time
from .abi import ABI
import json
class AISmartContract:
    _EVENTS = []  # To be overridden by child contracts
    
    def __init__(self, address):
        self.address = address
        self.events = []
        self.abi = ABI.generate(self.__class__)
        
    def get_abi(self) -> str:
        """Returns JSON-formatted ABI"""
        return json.dumps(self.abi, indent=2)
        
    def _emit_event(self, event_name, data):
        """Standard event emission with timestamp"""
        self.events.append({
            'event': event_name,
            'data': data,
            'timestamp': time.time(),
            'contract_address': self.address
        })
        
    def execute(self, function_name, *args, **kwargs):
        """To be implemented by child contracts"""
        raise NotImplementedError