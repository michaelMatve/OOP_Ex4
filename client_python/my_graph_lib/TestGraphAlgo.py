from unittest import TestCase
from GraphAlgo import GraphAlgo
from DiGraph import DiGraph


class TestGraphAlgo(TestCase):

    def make_my_graph(self):
        my_algo = GraphAlgo()
        my_algo.graph.add_node(0, (1.1, 1.5, 0))
        my_algo.graph.add_node(2, (1.4, 1.3, 0))
        my_algo.graph.add_node(5,(1.1, 0.5, 0))
        my_algo.graph.add_node(6, (1.3, 1, 0))
        my_algo.graph.add_node(7, (1.5, 0.8, 0))
        my_algo.graph.add_node(10, (2.0, 1.1, 0))
        my_algo.graph.add_node(12,(2.5, 1.4, 0))
        my_algo.graph.add_node(13, (1.3, 0.3, 0))
        my_algo.graph.add_edge(0, 2, 1.2)
        my_algo.graph.add_edge(2, 0, 2.5)
        my_algo.graph.add_edge(2, 10, 1.8)
        my_algo.graph.add_edge(6, 2, 1.3)
        my_algo.graph.add_edge(6, 5, 1.4)
        my_algo.graph.add_edge(5, 7, 0.2)
        my_algo.graph.add_edge(7, 13, 2.6)
        my_algo.graph.add_edge(13, 10, 1.85)
        my_algo.graph.add_edge(10, 6, 1.1)
        my_algo.graph.add_edge(10, 7, 1.32)
        my_algo.graph.add_edge(10, 12, 1.0)
        my_algo.graph.add_edge(12, 13, 1.7)
        return my_algo

    def test_get_graph(self):
        my_algo_in = self.make_my_graph()
        my_graph = my_algo_in.get_graph()
        self.assertEqual(my_graph.num_edges, my_algo_in.graph.num_edges)
        self.assertEqual(my_graph.num_nodes, my_algo_in.graph.num_nodes)
        self.assertEqual(my_graph.nodes.get(0).out_edges.get(2), my_algo_in.graph.nodes.get(0).out_edges.get(2))
        self.assertEqual(my_graph.nodes.get(13).in_edges.get(7), my_algo_in.graph.nodes.get(13).in_edges.get(7))


    def test_load_from_json(self):
        my_algo_in = self.make_my_graph()
        my_algo_in.save_to_json('testLoad.json')
        my_algo_js = GraphAlgo()
        self.assertEqual(my_algo_js.load_from_json('testLoad.json'),True)
        self.assertEqual(my_algo_js.graph.num_edges,my_algo_in.graph.num_edges)
        self.assertEqual(my_algo_js.graph.num_nodes, my_algo_in.graph.num_nodes)
        self.assertEqual(my_algo_js.graph.nodes.get(0).out_edges.get(2), my_algo_in.graph.nodes.get(0).out_edges.get(2))
        self.assertEqual(my_algo_js.graph.nodes.get(13).in_edges.get(7), my_algo_in.graph.nodes.get(13).in_edges.get(7))

        graph = GraphAlgo()
        # graph.load_from_json("..\\data\\n1000.json")
        # graph.load_from_json("..\\data\\n10000.json")
        # graph.load_from_json("..\\data\\n100000.json")



    def test_save_to_json(self):
        my_algo_in = self.make_my_graph()
        my_algo_in.save_to_json('testLoad.json')
        my_algo_js = GraphAlgo()
        self.assertEqual(my_algo_js.load_from_json('testLoad.json'), True)
        self.assertEqual(my_algo_js.graph.num_edges, my_algo_in.graph.num_edges)
        self.assertEqual(my_algo_js.graph.num_nodes, my_algo_in.graph.num_nodes)
        self.assertEqual(my_algo_js.graph.nodes.get(0).out_edges.get(2), my_algo_in.graph.nodes.get(0).out_edges.get(2))
        self.assertEqual(my_algo_js.graph.nodes.get(13).in_edges.get(7), my_algo_in.graph.nodes.get(13).in_edges.get(7))

        graph = GraphAlgo()


    def test_shortest_path(self):
        my_algo_in = self.make_my_graph()
        self.assertEqual(my_algo_in.shortest_path(0,10)[0], 3)
        self.assertEqual(my_algo_in.shortest_path(0, 10)[1], [0,2,10])
        self.assertEqual(my_algo_in.shortest_path(0, 12)[0], 4)
        self.assertEqual(my_algo_in.shortest_path(0, 12)[1], [0,2,10,12])
        self.assertEqual(my_algo_in.shortest_path(0, 5)[0], 5.5)
        self.assertEqual(my_algo_in.shortest_path(0, 5)[1], [0,2,10,6,5])

        self.assertEqual(my_algo_in.shortest_path(5, 6)[0], 5.75)
        self.assertEqual(my_algo_in.shortest_path(5, 6)[1], [5,7,13,10,6])
        self.assertEqual(my_algo_in.shortest_path(5, 12)[0], 5.65)
        self.assertEqual(my_algo_in.shortest_path(5, 12)[1], [5,7,13,10,12])
        self.assertEqual(my_algo_in.shortest_path(5, 10)[0], 4.65)
        self.assertEqual(my_algo_in.shortest_path(5, 10)[1], [5,7,13,10])

    def test_tsp(self):
        my_algo_in = self.make_my_graph()
        self.assertEqual(my_algo_in.TSP([12,0, 10, 6])[1], 8.45)
        self.assertEqual((my_algo_in.TSP([12,0, 10, 6])[0]), [12,13,10,6,2,0])
        my_algo_in.dijkstra_algo(13)
        self.assertEqual(my_algo_in.TSP([0,12,10,6])[1], 8.65)
        self.assertEqual(my_algo_in.TSP([0,12,10,6])[0], [0,2,10,12,13,10,6])

        # graph = GraphAlgo()
        # graph.load_from_json("nss1000.json")
        # self.assertEqual((graph.TSP([12,0, 10, 6])[0]), [12, 765, 346, 10, 200, 88, 6, 329, 54, 0])





    def test_centerPoint(self):
        my_algo_in = self.make_my_graph()
        self.assertEqual(my_algo_in.centerPoint()[0],6)
        self.assertEqual(my_algo_in.centerPoint()[1], 4.2)

        # graph = GraphAlgo()
        # graph.load_from_json("nss1000.json")
        # self.assertEqual(245, graph.centerPoint()[0])



    def test_plot_graph(self):
        my_algo_in = self.make_my_graph()
        my_algo_in.plot_graph()

    def test_random_pos(self):
        my_algo_in = self.make_my_graph()
        self.assertEqual(((my_algo_in.random_pos())[0]>35.187594216303474), True)
        self.assertEqual(((my_algo_in.random_pos())[0] > 35.21310882485876), False)
        self.assertEqual(((my_algo_in.random_pos())[1] < 32.10788938151261), True)
        self.assertEqual(((my_algo_in.random_pos())[1] < 32.10152879327731), False)


    def test_to_json_file(self):
        my_algo_in = self.make_my_graph()
        dict = my_algo_in.to_json_file()
        self.assertEqual(len(dict['Edges']), my_algo_in.graph.num_edges)
        self.assertEqual(len(dict['Nodes']), my_algo_in.graph.num_nodes)

    def test_dijkstra_algo(self):
        my_algo_in = self.make_my_graph()
        my_algo_in.dijkstra_algo(0)
        self.assertEqual(my_algo_in.graph.nodes.get(10).weight,3)
        self.assertEqual(my_algo_in.graph.nodes.get(12).weight, 4)
        self.assertEqual(my_algo_in.graph.nodes.get(5).weight, 5.5)
        my_algo_in.dijkstra_algo(5)
        self.assertEqual(my_algo_in.graph.nodes.get(6).weight, 5.75)
        self.assertEqual(my_algo_in.graph.nodes.get(12).weight, 5.65)
        self.assertEqual(my_algo_in.graph.nodes.get(10).weight, 4.65)

    def test_max_dist(self):
        my_algo_in = self.make_my_graph()
        self.assertEqual(my_algo_in.max_dist(0), 5.7)
        self.assertEqual(my_algo_in.max_dist(6), 4.2)

    def test_dfs(self):
        my_algo_in = self.make_my_graph()
        my_algo_in.dfs(my_algo_in.graph.nodes.get(0))
        self.assertEqual(my_algo_in.graph.nodes.get(6).tag,1)
        self.assertEqual(my_algo_in.graph.nodes.get(13).tag,1)
        my_algo_in.graph.remove_edge(0,2)
        my_algo_in.set_tags_weight()
        my_algo_in.dfs(my_algo_in.graph.nodes.get(0))
        self.assertEqual(my_algo_in.graph.nodes.get(6).tag, -1)
        self.assertEqual(my_algo_in.graph.nodes.get(13).tag, -1)


    def test_get_transpose(self):
        my_algo_in = self.make_my_graph()
        my_algo_tr = self.make_my_graph()
        my_algo_tr.get_transpose()
        self.assertEqual(my_algo_tr.graph.num_edges, my_algo_in.graph.num_edges)
        self.assertEqual(my_algo_tr.graph.num_nodes, my_algo_in.graph.num_nodes)
        self.assertEqual(my_algo_tr.graph.nodes.get(0).in_edges.get(2), my_algo_in.graph.nodes.get(0).out_edges.get(2))
        self.assertEqual(my_algo_tr.graph.nodes.get(13).out_edges.get(7), my_algo_in.graph.nodes.get(13).in_edges.get(7))

    def test_set_tags_weight(self):
        my_algo_in = self.make_my_graph()
        my_algo_in.set_tags_weight()
        self.assertEqual(my_algo_in.graph.nodes.get(6).tag, -1)
        self.assertEqual(my_algo_in.graph.nodes.get(10).info, 'w')
        self.assertEqual(my_algo_in.graph.nodes.get(0).weight, float('inf'))
        self.assertEqual(my_algo_in.graph.nodes.get(2).tag, -1)

    def test_is_connected(self):
        my_algo_in = self.make_my_graph()
        self.assertEqual(my_algo_in.is_connected(), True)
        my_algo_in.graph.remove_node(0)
        self.assertEqual(my_algo_in.is_connected(), True)
        my_algo_in.graph.remove_edge(6, 2)
        self.assertEqual(my_algo_in.is_connected(), False)
