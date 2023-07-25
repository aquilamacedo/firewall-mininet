from logging import info, warning, error, debug
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt

from pox.core import core
from pox.lib.revent import *
from pox.lib.addresses import EthAddr, IPAddr
from pox.lib.revent.revent import EventMixin
import json

# Constants for rule types
ETH_RULE = "eth"
TCP_RULE = "tcp"

# Default rules JSON file
DEFAULT_RULES = "firewall_rules_config.json"

class SDNFirewall(EventMixin):
  def __init__(self, rules, router_id):
    self.listenTo(core.openflow)
    self.rules = rules
    self.router_id = router_id

  def _handle_ConnectionUp(self, event):
    if event.dpid == self.router_id:
      for rule in self.rules:
        add_rule(event, rule)
      info("Firewall set up in switch %s" % firewall_router_id)

def add_eth_rule(rule, block):
  if isinstance(rule, dict):
    block.dl_src = EthAddr(rule.get("src"))
    block.dl_dst = EthAddr(rule.get("dst"))
  elif isinstance(rule, list):
    block.dl_src = EthAddr(rule[0])
    block.dl_dst = EthAddr(rule[1])
  else:
    warning("Invalid eth rule format, ignoring it")
    return

  debug("Added eth rule: " + str(rule))

def _add_tp_rule(rule, block, name):
  if isinstance(rule, dict):
    if "src" in rule:
      block.tp_src = int(rule["src"])
    if "dst" in rule:
      block.tp_dst = int(rule["dst"])
  elif isinstance(rule, list):
    try:
      block.tp_src = int(rule[0])
      block.tp_dst = int(rule[1])
    except IndexError:
      pass
  else:
    warning("Invalid" + name + "rule format, ignoring it")
    return
  debug("Added " + name + " rule: " + str(rule))

def add_tcp_rule(rule, block):
  block.dl_type = pkt.ethernet.IP_TYPE
  block.nw_proto = pkt.ipv4.TCP_PROTOCOL
  _add_tp_rule(rule, block, "TCP")

def warn_inconsistent_rule(rule):
  if "tcp" in rule and "udp" in rule:
    warning("Rule has both TCP and UDP, behavior is undefined")

def add_rule(event, rule):
  block = of.ofp_match()
  warn_inconsistent_rule(rule)

  for rule_type in rule:
    if rule_type == ETH_RULE:
      add_eth_rule(rule[ETH_RULE], block)
    elif rule_type == TCP_RULE:
      add_tcp_rule(rule[TCP_RULE], block)

  block_rule = of.ofp_flow_mod()
  block_rule.match = block
  event.connection.send(block_rule)

def launch(rules=DEFAULT_RULES, router_id=1):
  try:
    with open(rules) as f:
      rules_json = json.load(f)
    core.getLogger().info("Loaded rules from " + rules)
    rules_list = rules_json.get("rules", [])
    firewall_router_id = int(router_id)
  except Exception as e:
    error("Could not load rules: " + str(e))

  core.registerNew(SDNFirewall, rules_list, firewall_router_id)
