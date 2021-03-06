"""
How Does DGL Represent A Graph?
===============================

By the end of this tutorial you will be able to:

-  Construct a graph in DGL from scratch.
-  Assign node and edge features to a graph.
-  Query properties of a DGL graph such as node degrees and
   connectivity.
-  Transform a DGL graph into another graph.
-  Load and save DGL graphs.

(Time estimate: 16 minutes)

"""


######################################################################
# DGL Graph Construction
# ----------------------
# 
# DGL represents a directed graph as a ``DGLGraph`` object. You can
# construct a graph by specifying the number of nodes in the graph as well
# as the list of source and destination nodes.  Nodes in the graph have
# consecutive IDs starting from 0.
# 
# For instance, the following code constructs a directed star graph with 5
# leaves. The center node's ID is 0. The edges go from the
# center node to the leaves.
# 

import dgl
import numpy as np
import torch

g = dgl.graph(([0, 0, 0, 0, 0], [1, 2, 3, 4, 5]), num_nodes=6) # first vector is source of each edge, second vector is destination of each edge; 
# Equivalently, PyTorch LongTensors also work.
g = dgl.graph((torch.LongTensor([0, 0, 0, 0, 0]), torch.LongTensor([1, 2, 3, 4, 5])), num_nodes=6)

# You can omit the number of nodes argument if you can tell the number of nodes from the edge list alone.
g = dgl.graph(([0, 0, 0, 0, 0], [1, 2, 3, 4, 5]))


######################################################################
# Edges in the graph have consecutive IDs starting from 0, and are
# in the same order as the list of source and destination nodes during
# creation.
# 

# Print the source and destination nodes of every edge.
print("-----------------------------------------------------------------------------------")
print("Step 1: DGL Graph Construction: ")
print("first vector is made up of sources, second vector is made up of destinations: ")
print(g.edges())


######################################################################
# .. note::
# 
#    ``DGLGraph``'s are always directed to best fit the computation
#    pattern of graph neural networks, where the messages sent
#    from one node to the other are often different between both
#    directions. If you want to handle undirected graphs, you may consider
#    treating it as a bidirectional graph. See `Graph
#    Transformations`_ for an example of making
#    a bidirectional graph.
# 


######################################################################
# Assigning Node and Edge Features to Graph
# -----------------------------------------
# 
# Many graph data contain attributes on nodes and edges.
# Although the types of node and edge attributes can be arbitrary in real
# world, ``DGLGraph`` only accepts attributes stored in tensors (with
# numerical contents). Consequently, an attribute of all the nodes or
# edges must have the same shape. In the context of deep learning, those
# attributes are often called *features*.
# 
# You can assign and retrieve node and edge features via ``ndata`` and
# ``edata`` interface.
# 

# Assign a 3-dimensional node feature vector for each node.
g.ndata['x'] = torch.randn(6, 3)  # ndatra is node; 
# Assign a 4-dimensional edge feature vector for each edge.
g.edata['a'] = torch.randn(5, 4)  # edata is edge; 
# Assign a 5x4 node feature matrix for each node.  Node and edge features in DGL can be multi-dimensional.
g.ndata['y'] = torch.randn(6, 5, 4)

print("-----------------------------------------------------------------------------------")
print("Step 2: Assigning Node and Edge Features to Graph: ")
print("edge feature vector: ")
print(g.edata['a'])


######################################################################
# .. note::
# 
#    The vast development of deep learning has provided us many
#    ways to encode various types of attributes into numerical features.
#    Here are some general suggestions:
# 
#    -  For categorical attributes (e.g.??gender, occupation), consider
#       converting them to integers or one-hot encoding.
#    -  For variable length string contents (e.g.??news article, quote),
#       consider applying a language model.
#    -  For images, consider applying a vision model such as CNNs.
# 
#    You can find plenty of materials on how to encode such attributes
#    into a tensor in the `PyTorch Deep Learning
#    Tutorials <https://pytorch.org/tutorials/>`__.
# 


######################################################################
# Querying Graph Structures
# -------------------------
# 
# ``DGLGraph`` object provides various methods to query a graph structure.
# 


print("-----------------------------------------------------------------------------------")
print("Step 3: Querying Graph Structures: ")
print("num nodes: ")
print(g.num_nodes())
print("num edges: ")
print(g.num_edges())
# Out degrees of the center node
print("out degree of 0: ")
print(g.out_degrees(0))
# In degrees of the center node - note that the graph is directed so the in degree should be 0.
print("in degree of 0: ")
print(g.in_degrees(0))

print("out degree of 2: ")
print(g.out_degrees(2))
print("in degree of 2: ")
print(g.in_degrees(2))

######################################################################
# Graph Transformations
# ---------------------
# 


######################################################################
# DGL provides many APIs to transform a graph to another such as
# extracting a subgraph:
# 

# Induce a subgraph from node 0, node 1 and node 3 from the original graph.
sg1 = g.subgraph([0, 1, 3])
# Induce a subgraph from edge 0, edge 1 and edge 3 from the original graph.
sg2 = g.edge_subgraph([0, 1, 3])


######################################################################
# You can obtain the node/edge mapping from the subgraph to the original
# graph by looking into the node feature ``dgl.NID`` or edge feature
# ``dgl.EID`` in the new graph.
# 

print("-----------------------------------------------------------------------------------")
print("Step 4: Graph Transformations")
# The original IDs of each node in sg1
print("original IDs of each node in sg1: ")
print(sg1.ndata[dgl.NID])
# The original IDs of each edge in sg1
print("original IDs of each edge in sg1: ")
print(sg1.edata[dgl.EID])
# The original IDs of each node in sg2
print("original IDs of each node in sg2: ")
print(sg2.ndata[dgl.NID])
# The original IDs of each edge in sg2
print("original IDs of each edge in sg2: ")
print(sg2.edata[dgl.EID])


######################################################################
# ``subgraph`` and ``edge_subgraph`` also copies the original features
# to the subgraph:
#

# The original node feature of each node in sg1
print("original node feature of each node in sg1: ")
print(sg1.ndata['x'])
# The original edge feature of each node in sg1
print("original edge feature of each node in sg1: ")
print(sg1.edata['a'])
# The original node feature of each node in sg2
print("original node feature of each node in sg2: ")
print(sg2.ndata['x'])
# The original edge feature of each node in sg2
print("original edge feature of each node in sg2: ")
print(sg2.edata['a'])


######################################################################
# Another common transformation is to add a reverse edge for each edge in
# the original graph with ``dgl.add_reverse_edges``.
# 
# .. note::
# 
#    If you have an undirected graph, it is better to convert it
#    into a bidirectional graph first via adding reverse edges.
# 

print("add reverse edges: ")
newg = dgl.add_reverse_edges(g)
newg.edges()


######################################################################
# Loading and Saving Graphs
# -------------------------
# 
# You can save a graph or a list of graphs via ``dgl.save_graphs`` and
# load them back with ``dgl.load_graphs``.
# 

# Save graphs
print("-----------------------------------------------------------------------------------")
print("Step 5: Loading and Saving Graphs: ")
dgl.save_graphs('graph.dgl', g)
dgl.save_graphs('graphs.dgl', [g, sg1, sg2])

# Load graphs
(g,), _ = dgl.load_graphs('graph.dgl')
print("graph g: ")
print(g)  # each graph contain nodes and their features, edges and their features; 
(g, sg1, sg2), _ = dgl.load_graphs('graphs.dgl')
print("graph g: ")
print(g)
print("graph sg1: ")
print(sg1)
print("graph sg2: ")
print(sg2)


######################################################################
# What???s next?
# ------------
# 
# -  See
#    :ref:`here <apigraph-querying-graph-structure>`
#    for a list of graph structure query APIs.
# -  See
#    :ref:`here <api-subgraph-extraction>`
#    for a list of subgraph extraction routines.
# -  See
#    :ref:`here <api-transform>`
#    for a list of graph transformation routines.
# -  API reference of :func:`dgl.save_graphs`
#    and
#    :func:`dgl.load_graphs`
# 


# Thumbnail Courtesy: Wikipedia
# sphinx_gallery_thumbnail_path = '_static/blitz_2_dglgraph.png'
