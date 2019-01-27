"""Visulize utils."""
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import polyvore.config as cfg


def visualize_kernel(data):
    """Visulize kernerl.

    Take an array of shape (n, height, width) or (n, height, width, 3) and
    visualize each (height, width) thing in a grid of size approx.
    sqrt(n) by sqrt(n)
    """
    # normalize data for display
    data = (data - data.min()) / (data.max() - data.min())
    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = (((0, n**2 - data.shape[0]), (0, 1),
                (0, 1)) + ((0, 0), ) * (data.ndim - 3))
    # tile the filters into an image
    data = np.pad(data, padding, mode='constant', constant_values=1)
    trans = (0, 2, 1, 3) + tuple(range(4, data.ndim + 1))
    data = data.reshape((n, n) + data.shape[1:]).transpose(trans)
    new_size = (n * data.shape[1], n * data.shape[3]) + data.shape[4:]
    data = data.reshape(new_size)
    plt.imshow(data)
    plt.axis('off')


class DataStatistic(object):
    """Statistic for dataset."""

    def __init__(self, tuple_dir):
        """Get data set."""
        tuple_dir = Path(tuple_dir)
        self.tuples = {
            p: pd.read_csv(self.tuple_dir / 'tuples_posi_{}'.format(p))
            for p in cfg.Phase
        }
        self.item_set = {
            p: list(map(set, tuples[0, 1:].transpose()))
            for p, tuples in self.tuples.items()
        }

    def show_repetition(self):
        """Show repetition.

        Show repetition of item in each pahse.
        """
        for idx, cate in enumerate(cfg.CateName):
            set_dict = {}
            for p in cfg.Phase:
                key = p + ' ' + cate
                set_dict[key] = self.item_set[p][idx]
            self.vis_repetition(set_dict)

    def load_items_set(self, tuples):
        """Load items in outfit.

        Given a file of tuples list, load id set of top, bottom and shoe
        for each user.
        """
        num_users = len(set(tuples[:, 0]))
        user_top = [set() for i in range(num_users)]
        user_bot = [set() for i in range(num_users)]
        user_sho = [set() for i in range(num_users)]
        for tpl in tuples:
            user_top[tpl[0]].add(tpl[1])
            user_bot[tpl[0]].add(tpl[2])
            user_sho[tpl[0]].add(tpl[3])
        return (num_users, user_top, user_bot, user_sho)

    def get_Graph(self, item_sets):
        """Get the graph of user w.r.t items."""
        num_users = len(item_sets)
        G = nx.Graph()
        H = nx.path_graph(num_users)
        G.add_nodes_from(H)
        for i in range(0, num_users):
            for j in range(i + 1, num_users):
                weight = len(item_sets[i] & item_sets[j])
                if weight > 0:
                    G.add_edge(i, j, weight=weight)
        return G

    def draw_user_item(self, tuples):
        """Draw figiure for user relation with items."""
        num_users, user_top, user_bot, user_sho = self.load_items_set(tuples)
        G = self.get_Graph(num_users, user_top)
        nx.draw_random(G)
        # plt.show()
        plt.savefig('top.png')
        G = self.get_Graph(num_users, user_bot)
        nx.draw_random(G)
        # plt.show()
        plt.savefig('bot.png')
        G = self.get_Graph(num_users, user_sho)
        nx.draw_random(G)
        # plt.show()
        plt.savefig('shoe.png')

    def vis_repetition(self, set_dict):
        """Visualize repetition.

        Parameter
        ---------
        dict: sets with name.

        """
        num_set = len(set_dict)
        keys = set_dict.keys()
        len_str = max([len(i) for i in keys])
        values = set_dict.values()
        rep_size = np.zeros((num_set, num_set), dtype=np.int)
        for i in range(num_set):
            rep_size[i][i] = len(values[i])
            for j in range(i + 1, num_set):
                rep_size[i][j] = len(values[i] & values[j])
                rep_size[j][i] = rep_size[i][j]
        info = ("{:^" + str(len_str) + "}") * (num_set + 2)
        info_value = [i for i in keys]
        info_value.insert(0, '')
        info_value.append('size')
        print(info.format(*info_value))
        for i in range(num_set):
            info_value = [rep_size[i][j] for j in range(num_set)]
            info_value.insert(0, keys[i])
            info_value.append(rep_size[i][i])
            print(info.format(*info_value))
