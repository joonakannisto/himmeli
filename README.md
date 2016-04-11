# Link watching script for Open vSwitch

VXLAN interfaces do not expose link state to the Openflow controller in Open vSwitch. 

This script watches a primary interface's IP layer reachability and removes the interface & the associated flows, when the IP layer connectivity breaks. 
