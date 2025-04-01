from .token import AITokenContract
from .base import AISmartContract
import time
from typing import Dict, List, Optional, Any  # Added type imports
from .abi import ABI
class ContractRegistry:
    CONTRACT_TYPES = {
        'token': AITokenContract,
        # Add other contract types here
    }
    
    def __init__(self):
        self.contracts = {}
        
    def deploy(self, contract_type, constructor_args=None):
        if contract_type not in self.CONTRACT_TYPES:
            raise ValueError(f"Unknown contract type: {contract_type}")
            
        contract_class = self.CONTRACT_TYPES[contract_type]
        contract = contract_class(self._generate_address(), **(constructor_args or {}))
        self.contracts[contract.address] = contract
        return contract.address
        
    def _generate_address(self):
        import hashlib
        return '0x' + hashlib.sha256(str(time.time()).encode()).hexdigest()[:40]
    
    def get_abi(self, contract_address: str) -> Optional[str]:
        """Returns ABI for a deployed contract"""
        contract = self.contracts.get(contract_address)
        return contract.get_abi() if contract else None

    def encode_transaction(self, contract_address: str, function_name: str, args: List) -> Optional[Dict]:
        """Generates ABI-encoded transaction"""
        if contract_address not in self.contracts:
            return None
            
        return {
            'to': contract_address,
            'data': ABI.encode_call(function_name, args),
            'abi': self.get_abi(contract_address)
        }