"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import torch
from torch import nn
import pmt


class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        #self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(10*2, 8*2),
            nn.Tanh(),
            nn.Linear(8*2, 4*2),
            nn.Tanh(),
            nn.Linear(4*2, 2)
        )

    def forward(self, x):
        if isinstance(x, np.ndarray):
            #x_real = np.stack((x.real, x.imag), axis=1).astype(np.float32)  # shape: [N, 2]
            #norms = np.linalg.norm(x_real, axis=1, keepdims=True) + 1e-8
            #x_real = x_real / norms
            xp = torch.from_numpy(x)
            logits = self.linear_relu_stack(xp)
            y = logits.detach().numpy().astype(np.complex64)
            complex_out = y[:, 0] + 1j * y[:, 1]
            return complex_out.astype(np.complex64)
        else:
            logits = self.linear_relu_stack(x)
            return logits  # return raw tensor, not converted to NumPy
    
class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Multi-Layer Perceptron Equalizer"""

    def __init__(self, training_sequence=[], tag_key = ''):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='MLPE',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.training_sequence = np.array(training_sequence, dtype=np.complex64)
        self.tag_key = tag_key
        self.model = NeuralNetwork().to("cpu")
        self.loss_fn = nn.MSELoss()
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=50e-3, momentum = 0.50, nesterov = False)
        self.wrap_sequence = np.zeros(19, dtype = np.float32)

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        in0 = input_items[0]
        n_items = len(in0)

        # get all tags associated with input_items[0]
        tagTuple = self.get_tags_in_window(0, 0, n_items)

        # loop through all input tags
        for tag in tagTuple:
            if (pmt.to_python(tag.key) == self.tag_key):
                self.model.train()
                abs_offset = tag.offset - self.nitems_read(0)
                train_len = len(self.training_sequence)
                if abs_offset + train_len <= n_items:
                    input_window = in0[abs_offset:abs_offset + train_len]
                    self.train_on_window(input_window, self.training_sequence)
                else:
                    input_window = in0[abs_offset::]
                    croped_sequence = self.training_sequence[:len(input_window)]
                    self.train_on_window(input_window, croped_sequence)
                  
        float_input = np.stack((in0.real, in0.imag), axis=1).astype(np.float32) #batch x 2
        #flat_input = np.concatenate((float_input.flatten(),np.zeros(19, dtype = np.float32)))
        flat_input = np.concatenate((self.wrap_sequence, float_input.flatten()))
        windowed_input = np.lib.stride_tricks.sliding_window_view(flat_input, 20)
        resized_input = windowed_input[::2]
        self.wrap_sequence = flat_input[(len(flat_input)-19)::]

        self.model.eval()
        output_items[0][:] = self.model(resized_input)
        return len(output_items[0])
    
    def train_on_window(self, input_data, target_data):
        #self.model.train()
        x = np.stack((input_data.real, input_data.imag), axis=1).astype(np.float32)
        y = np.stack((target_data.real, target_data.imag), axis=1).astype(np.float32)
        #x_flat = np.concatenate((x.flatten(),np.zeros(19, dtype = np.float32)))
        x_flat = np.concatenate((self.wrap_sequence, x.flatten()))
        x_window =  np.lib.stride_tricks.sliding_window_view(x_flat, 20)
        x_resize = x_window[::2]

        x_tensor = torch.from_numpy(x_resize)
        y_tensor = torch.from_numpy(y)

        pred = self.model(x_tensor)

        loss = self.loss_fn(pred[:(len(pred)-20)], y_tensor[:(len(y_tensor)-20)])

        loss.backward()
        self.optimizer.step()
        self.optimizer.zero_grad()


