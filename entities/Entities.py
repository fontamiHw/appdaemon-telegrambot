'''
Created on Feb 11, 2024

@author: mfontane
'''
import re

class Entities(object):
    '''
    classdocs
    '''

    def __init__(self, bot, entityFilter, extendEntity, entityType, icon, statedict):      
      self.bot = bot
      self.entityFilter = entityFilter
      self.entityType = entityType
      self.statedict = statedict
            
      entityDict={
                   f"/{icon}{self.entityType}_state": {"desc": f"State of {self.entityType}", "method": self._cmd_state_entity},
                   f"/{icon}{self.entityType}_off": {"desc": f"Turn off {self.entityType}", "method": self._cmd_turn_off_entity},
                   f"/{icon}{self.entityType}_on": {"desc": f"Turn on {self.entityType}", "method": self._cmd_turn_on_entity}
                 }            
      entityClb = {
                   f"/clb_turnoff_{self.entityType}": {"desc": f"Turn off {self.entityType}", "method": self._clb_turn_off_entity},
                   f"/clb_turnon_{self.entityType}": {"desc": f"Turn on {self.entityType}", "method": self._clb_turn_on_entity}
                  }
      self.bot._commanddict.update(entityDict)
      self.bot._callbackdict.update(entityClb)

      
      self.extendEntity = list()
      if self.bot.args.get(extendEntity,None) is not None and self.bot.args.get(extendEntity)!="":
        self.extendEntity=self.bot.args[extendEntity].split(',')
      self.bot._log_debug(f"{extendEntity}: {self.extendEntity}")
        

    
    def send_message(self, msg, target_id):
      self.bot._log_debug(msg)
      self.bot._send_message(msg, target_id)
            
    def _cmd_state_entity(self, target_id):
      self.statedict = self.bot._get_state_filtered()
      statedict = self.statedict
      msg=""
      for entity in statedict:
        if re.match(self.entityFilter, entity, re.IGNORECASE):
          self.bot._log_debug(statedict.get(entity))
          state = statedict.get(entity).get("state")
          desc = self.bot._getid(statedict,entity)
          msg += f"{desc}\nstate: {state}\n\n"

      for entity in self.extendEntity:
        l = entity.strip()
        self.bot._log_debug(l)
        state = self.bot.get_state(l)
        desc = self.bot._getid(statedict, l)
        msg += f"{desc}\nstate: {state}\n\n"

      self.send_message(msg, target_id)
      
  
    def _cmd_turn_off_entity(self, target_id):
        msg = f"Which {self.entityType} do you want to turn off?\n\n"
        statedict = self.statedict
        keyboard_options=list()
        keyboard_options.append({
                    'description': f"Turn off all {self.entityType}",
                    'url':f"/clb_turnoff_{self.entityType}?entity_id=all"})
        for entity in statedict:
            if re.match(self.entityFilter, entity, re.IGNORECASE):
                self.bot._log_debug(statedict.get(entity))
                hashvalue = self.bot._get_hash_from_entityid(entity)
                desc = self.bot._getid(statedict,entity)
                keyboard_options.append({
                    'description': f"{desc}",
                    'url':f"/clb_turnoff_{self.entityType}?entity_id={hashvalue}"})

        for entity in self.extendEntity:
            self.bot._log_debug(statedict.get(entity))
            hashvalue = self.bot._get_hash_from_entityid(entity)
            desc = self.bot._getid(statedict,entity)
            keyboard_options.append({
                'description': f"{desc}",
                'url':f"/clb_turnoff_{self.entityType}?entity_id={hashvalue}"})

        self.bot._build_keyboard_answer(keyboard_options, target_id, msg,)

    def _cmd_turn_on_entity(self, target_id):
        msg = f"Which {self.entityType} do you want to turn on?\n\n"
        statedict = self.statedict #self._get_state_filtered()
        keyboard_options=list()
        keyboard_options.append({
                    'description': f"Turn on all {self.entityType}",
                    'url':f"/clb_turnon_{self.entityType}?entity_id=all"})
        for entity in statedict:
            if re.match(self.entityFilter, entity, re.IGNORECASE):
              self.bot._log_debug(statedict.get(entity))
              hashvalue = self.bot._get_hash_from_entityid(entity)
              desc = self.bot._getid(statedict,entity)
              keyboard_options.append({
                    'description': f"{desc}",
                    'url':f"/clb_turnon_{self.entityType}?entity_id={hashvalue}"})

        for entity in self.extendEntity:
            self.bot._log_debug(statedict.get(entity))
            hashvalue = self.bot._get_hash_from_entityid(entity)
            desc = self.bot._getid(statedict,entity)
            keyboard_options.append({
                'description': f"{desc}",
                'url':f"/clb_turnon_{self.entityType}?entity_id={hashvalue}"})

        self.bot._build_keyboard_answer(keyboard_options, target_id, msg)

    def _clb_turn_off_entity(self, target_id, paramdict):
        hashvalue = paramdict.get("entity_id")
        entity_id = self.bot._get_entityid_from_hash(hashvalue)
        if hashvalue == "all":
          self._entity_all(target_id, "turn_off", "Turn off")
        elif entity_id is not None:
          self._entity_id(target_id, entity_id,  "Turn off")
          self._call_service(entity_id, "off")
        else:
          self._error_Entity(msg, target_id)

    def _clb_turn_on_entity(self, target_id, paramdict):
        hashvalue = paramdict.get("entity_id")
        entity_id = self.bot._get_entityid_from_hash(hashvalue)
        if hashvalue == "all":
          self._entity_all(target_id, "turn_on", "Turn on")
        elif entity_id is not None:
          self._entity_id(target_id, entity_id,  "Turn on")
          self._call_service(entity_id, "on")
        else:
          self._error_Entity(target_id)
            
            
    def _call_service(self, entity_id, on_off):
      if re.match('^light.*', entity_id, re.IGNORECASE):
        self.bot.call_service(f"light/turn_{on_off}", entity_id=entity_id)
      elif re.match('^switch.*', entity_id, re.IGNORECASE):
        self.bot.call_service(f"switch/turn_{on_off}", entity_id=entity_id)
      elif re.match('^input_boolean.*', entity_id, re.IGNORECASE):
        self.bot.call_service(f"input_boolean/turn_{on_off}", entity_id=entity_id)
    
    def _entity_all(self, target_id, cmd, cmdMsg):
      self.bot.call_service(f"{self.entityType}/{cmd}", entity_id="all")
      msg = f"{cmdMsg} all {self.entityType}!"
      self.bot._send_message(msg, target_id)
      self.bot.call_service(
          'telegram_bot/answer_callback_query',
          message=self.bot._escape_markdown(msg),
          callback_query_id=target_id)
    
    def _entity_id(self, target_id, entity_id, cmdMsg):
      friendly_name = self.bot.get_state(entity_id, attribute="friendly_name")
      msg=f"{cmdMsg} {self.entityType} {entity_id} ({friendly_name})"
      self.bot._send_message(msg, target_id)
      self.bot.call_service(
          'telegram_bot/answer_callback_query',
          message=self.bot._escape_markdown(msg),
          callback_query_id=target_id)
                    
    def _error_Entity(self, target_id):
      msg = "Unkown entity. Please do not resent old commands!"
      self.bot._send_message(msg, target_id)
      self.bot.call_service(
          'telegram_bot/answer_callback_query',
          message=self.bot._escape_markdown(msg),
          callback_query_id=target_id,
          show_alert=True)