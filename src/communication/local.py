from database.mash_db import MashDB
import bluetooth
import json

class MessageItem(object):

  def __init__(self, unit):
    self.sample_id = unit['data'][0]
    
    if unit['type'] == 'sample':
      self.type = 'sample'
      self.highest_matches = unit['data'][1]
    elif unit['type'] == 'update':
      self.type = 'update'
      self.globally_shared = True
    else:
      raise Exception("Something is wrong with the type of the messageItem")
    self.data = unit['data']

class Message(object):
  """
  Data structure that holds a message used to transfer data between peers, it follows a JSON strcture:

  {
    "message": [
      {
        "type": <"sample">||<"update">,
        "data": [<"sample_id">, <"highest_matches">||<"globally_shared">]
       },
       ...
    ]
    "sender": <"bd_addr">
  }
  """
  def __init__(self, data):
    json_data = json.loads(data)
    self.message = json_data['message']
    self.sender = json_data['sender']
    self.items = []
    for item in self.message:
      self.items.append(MessageItem(item))
    
  def __str__(self):
    return "Sender: {} \n Message: {}".format(self.sender, self.message)



class LocalCommunication(object):

  def __init__(self):
    self.mash_db = MashDB()

  def find_local_peers(self):
    print "Looking for nearby devices..."

    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    
    print("found %d devices" % len(nearby_devices))
    
    for addr, name in nearby_devices:
      print("  %s - %s" % (addr, name))

    return nearby_devices

  def get_data_from_peer(self):

    server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    port = 1
    server_sock.bind(("",port))
    server_sock.listen(1)

    client_sock,address = server_sock.accept()
    print "Accepted connection from ",address

    data = Message(client_sock.recv(1024))
    print "received [%s]" % data

    print "Handling the message..."

    self.handle_message(data)

    client_sock.close()
    server_sock.close()

  def handle_message(self, msg):

    for item in msg.items:

      if item.type == "sample":
        print "I will add this sample to the db"
        self.mash_db.save_sample_result(item.sample_id, item.highest_matches)

      elif item.type == "update":
        print "If I have this ID, I will update, otherwise I will ignore"

