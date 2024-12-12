#!/usr/bin/env python3
import json
from helpers.get_users import get_users

print(json.dumps(get_users(), sort_keys=True, indent=2, default=str))