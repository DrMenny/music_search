from loko_extensions.model.components import Arg, Component, save_extensions, Input, Output, Select, Dynamic

output = Output(id='output', label='Output')
input_f = Input(id='file', label='Audio', service='upload_file', to='output')
input_w = Input(id='info', label='Info', service='wikipedia_info', to='output')
comp1 = Component(name='Music Search', inputs=[input_f, input_w], outputs=[output], icon='RiMusic2Fill')
save_extensions([comp1])