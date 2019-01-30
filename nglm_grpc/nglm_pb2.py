# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: nglm_grpc/nglm.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='nglm_grpc/nglm.proto',
  package='nglm_grpc',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x14nglm_grpc/nglm.proto\x12\tnglm_grpc\"H\n\nclientInfo\x12\x10\n\x08hostname\x18\x01 \x01(\t\x12\x0c\n\x04ipv4\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\x05\x12\x0c\n\x04uuid\x18\x04 \x01(\t\"1\n\x10registerResponse\x12\x0c\n\x04uuid\x18\x01 \x01(\t\x12\x0f\n\x07success\x18\x02 \x01(\x08\"\x1b\n\x08response\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x16\n\x05query\x12\r\n\x05query\x18\x01 \x01(\t\"\x19\n\tchunkSize\x12\x0c\n\x04size\x18\x01 \x01(\x01\"Z\n\x06params\x12\x0b\n\x03pid\x18\x01 \x01(\x05\x12\r\n\x05pname\x18\x02 \x01(\t\x12\x10\n\x08interval\x18\x03 \x01(\x05\x12\x10\n\x08\x64uration\x18\x04 \x01(\x05\x12\x10\n\x08taskUUID\x18\x05 \x01(\t\"\x18\n\x06\x63hunks\x12\x0e\n\x06\x62uffer\x18\x01 \x01(\x0c\x32~\n\x06Server\x12@\n\x08register\x12\x15.nglm_grpc.clientInfo\x1a\x1b.nglm_grpc.registerResponse\"\x00\x12\x32\n\x07isAlive\x12\x10.nglm_grpc.query\x1a\x13.nglm_grpc.response\"\x00\x32\xe5\x01\n\x07Logging\x12\x31\n\x05start\x12\x11.nglm_grpc.params\x1a\x13.nglm_grpc.response\"\x00\x12\x34\n\x06output\x12\x11.nglm_grpc.chunks\x1a\x13.nglm_grpc.response\"\x00(\x01\x12\x38\n\tgetConfig\x12\x14.nglm_grpc.chunkSize\x1a\x11.nglm_grpc.chunks\"\x00\x30\x01\x12\x37\n\tsetConfig\x12\x11.nglm_grpc.chunks\x1a\x13.nglm_grpc.response\"\x00(\x01\x62\x06proto3')
)




_CLIENTINFO = _descriptor.Descriptor(
  name='clientInfo',
  full_name='nglm_grpc.clientInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='hostname', full_name='nglm_grpc.clientInfo.hostname', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ipv4', full_name='nglm_grpc.clientInfo.ipv4', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='nglm_grpc.clientInfo.port', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='uuid', full_name='nglm_grpc.clientInfo.uuid', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=35,
  serialized_end=107,
)


_REGISTERRESPONSE = _descriptor.Descriptor(
  name='registerResponse',
  full_name='nglm_grpc.registerResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uuid', full_name='nglm_grpc.registerResponse.uuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='success', full_name='nglm_grpc.registerResponse.success', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=109,
  serialized_end=158,
)


_RESPONSE = _descriptor.Descriptor(
  name='response',
  full_name='nglm_grpc.response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='nglm_grpc.response.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=160,
  serialized_end=187,
)


_QUERY = _descriptor.Descriptor(
  name='query',
  full_name='nglm_grpc.query',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='query', full_name='nglm_grpc.query.query', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=189,
  serialized_end=211,
)


_CHUNKSIZE = _descriptor.Descriptor(
  name='chunkSize',
  full_name='nglm_grpc.chunkSize',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='size', full_name='nglm_grpc.chunkSize.size', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=213,
  serialized_end=238,
)


_PARAMS = _descriptor.Descriptor(
  name='params',
  full_name='nglm_grpc.params',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pid', full_name='nglm_grpc.params.pid', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pname', full_name='nglm_grpc.params.pname', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='interval', full_name='nglm_grpc.params.interval', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='duration', full_name='nglm_grpc.params.duration', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='taskUUID', full_name='nglm_grpc.params.taskUUID', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=240,
  serialized_end=330,
)


_CHUNKS = _descriptor.Descriptor(
  name='chunks',
  full_name='nglm_grpc.chunks',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='buffer', full_name='nglm_grpc.chunks.buffer', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=332,
  serialized_end=356,
)

DESCRIPTOR.message_types_by_name['clientInfo'] = _CLIENTINFO
DESCRIPTOR.message_types_by_name['registerResponse'] = _REGISTERRESPONSE
DESCRIPTOR.message_types_by_name['response'] = _RESPONSE
DESCRIPTOR.message_types_by_name['query'] = _QUERY
DESCRIPTOR.message_types_by_name['chunkSize'] = _CHUNKSIZE
DESCRIPTOR.message_types_by_name['params'] = _PARAMS
DESCRIPTOR.message_types_by_name['chunks'] = _CHUNKS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

clientInfo = _reflection.GeneratedProtocolMessageType('clientInfo', (_message.Message,), dict(
  DESCRIPTOR = _CLIENTINFO,
  __module__ = 'nglm_grpc.nglm_pb2'
  # @@protoc_insertion_point(class_scope:nglm_grpc.clientInfo)
  ))
_sym_db.RegisterMessage(clientInfo)

registerResponse = _reflection.GeneratedProtocolMessageType('registerResponse', (_message.Message,), dict(
  DESCRIPTOR = _REGISTERRESPONSE,
  __module__ = 'nglm_grpc.nglm_pb2'
  # @@protoc_insertion_point(class_scope:nglm_grpc.registerResponse)
  ))
_sym_db.RegisterMessage(registerResponse)

response = _reflection.GeneratedProtocolMessageType('response', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSE,
  __module__ = 'nglm_grpc.nglm_pb2'
  # @@protoc_insertion_point(class_scope:nglm_grpc.response)
  ))
_sym_db.RegisterMessage(response)

query = _reflection.GeneratedProtocolMessageType('query', (_message.Message,), dict(
  DESCRIPTOR = _QUERY,
  __module__ = 'nglm_grpc.nglm_pb2'
  # @@protoc_insertion_point(class_scope:nglm_grpc.query)
  ))
_sym_db.RegisterMessage(query)

chunkSize = _reflection.GeneratedProtocolMessageType('chunkSize', (_message.Message,), dict(
  DESCRIPTOR = _CHUNKSIZE,
  __module__ = 'nglm_grpc.nglm_pb2'
  # @@protoc_insertion_point(class_scope:nglm_grpc.chunkSize)
  ))
_sym_db.RegisterMessage(chunkSize)

params = _reflection.GeneratedProtocolMessageType('params', (_message.Message,), dict(
  DESCRIPTOR = _PARAMS,
  __module__ = 'nglm_grpc.nglm_pb2'
  # @@protoc_insertion_point(class_scope:nglm_grpc.params)
  ))
_sym_db.RegisterMessage(params)

chunks = _reflection.GeneratedProtocolMessageType('chunks', (_message.Message,), dict(
  DESCRIPTOR = _CHUNKS,
  __module__ = 'nglm_grpc.nglm_pb2'
  # @@protoc_insertion_point(class_scope:nglm_grpc.chunks)
  ))
_sym_db.RegisterMessage(chunks)



_SERVER = _descriptor.ServiceDescriptor(
  name='Server',
  full_name='nglm_grpc.Server',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=358,
  serialized_end=484,
  methods=[
  _descriptor.MethodDescriptor(
    name='register',
    full_name='nglm_grpc.Server.register',
    index=0,
    containing_service=None,
    input_type=_CLIENTINFO,
    output_type=_REGISTERRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='isAlive',
    full_name='nglm_grpc.Server.isAlive',
    index=1,
    containing_service=None,
    input_type=_QUERY,
    output_type=_RESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SERVER)

DESCRIPTOR.services_by_name['Server'] = _SERVER


_LOGGING = _descriptor.ServiceDescriptor(
  name='Logging',
  full_name='nglm_grpc.Logging',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  serialized_start=487,
  serialized_end=716,
  methods=[
  _descriptor.MethodDescriptor(
    name='start',
    full_name='nglm_grpc.Logging.start',
    index=0,
    containing_service=None,
    input_type=_PARAMS,
    output_type=_RESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='output',
    full_name='nglm_grpc.Logging.output',
    index=1,
    containing_service=None,
    input_type=_CHUNKS,
    output_type=_RESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='getConfig',
    full_name='nglm_grpc.Logging.getConfig',
    index=2,
    containing_service=None,
    input_type=_CHUNKSIZE,
    output_type=_CHUNKS,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='setConfig',
    full_name='nglm_grpc.Logging.setConfig',
    index=3,
    containing_service=None,
    input_type=_CHUNKS,
    output_type=_RESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_LOGGING)

DESCRIPTOR.services_by_name['Logging'] = _LOGGING

# @@protoc_insertion_point(module_scope)
