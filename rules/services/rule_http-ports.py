import time
from core.redis   import rds
from core.parser  import ScanParser, ConfParser
from core.triage  import Triage
from db.db_ports   import http_ports, https_ports

class Rule:
  def __init__(self):
    self.rule = 'SVC_ZGZA'
    self.rule_severity = 1
    self.rule_description = 'Checks for HTTP Ports'
    self.rule_confirm = 'Remote Server Exposes HTTP Port(s)'
    self.rule_details = ''
    self.rule_mitigation = '''Bind all possible network services to localhost, and configure only those which require remote clients on an external interface.'''
    self.intensity = 0

  def check_rule(self, ip, port, values, conf):
    c = ConfParser(conf)
    t = Triage()
    p = ScanParser(port, values)
    
    domain = p.get_domain()
    
    if port in http_ports or port in https_ports:
      self.rule_details = 'Open Port: {} (HTTP)'.format(port)
            
      js_data = {
          'ip':ip,
          'port':port,
          'domain':domain,
          'rule_id':self.rule,
          'rule_sev':self.rule_severity,
          'rule_desc':self.rule_description,
          'rule_confirm':self.rule_confirm,
          'rule_details':self.rule_details,
          'rule_mitigation':self.rule_mitigation
        }
        
      rds.store_vuln(js_data)
      
    return
