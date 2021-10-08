from math import ceil
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib import patches
import lattice_paths as lp

# paths = ("EEEENNN", "EEENENN", "NNENEEE")
# paths = {'blue': ("EEEENNN", "EEENENN", "NNENEEE"), 'green': ("NNEENEE", "EENNENE", "NNNEEEE")}
set1 = set(('EEEENNN', 'EENENNE', 'ENENEEN', 'ENNENEE', 'NEEEENN', 'NNEEENE'))
set2 = set(('EEEENNN', 'EENENNE', 'ENENNEE', 'ENNEEEN', 'NEEEENN', 'NENNEEE', 'NNEEENE'))
paths = {'blue': tuple(set1.difference(set2)), 'orange': tuple(set2.difference(set1)), 'green': tuple(set1.intersection(set2))}



def path_to_ints(path):
    last = path[0]
    count = 1
    out = []
    for i, x in enumerate(path[1:]):
        if x == last:
            count += 1
        else:
            out.append(count * ((-1) ** (last == 'N')))
            count = 1
            last = x
        if i==len(path)-2:
            out.append(count*((-1)**(last=='N')))
    return out

def offset_location_list(path_ints,filled_locs,path_edges):
    groups = []
    cumulative = 0
    for i in path_ints:
        groups.append(path_edges[cumulative:cumulative+abs(i)])
        cumulative += abs(i)
    offset_locs = []
    for group in groups:
        filled = [spot for l in group for spot in filled_locs[l]]
        loc = 0
        while True:
            if ceil(loc/2.0)*((-1)**(loc % 2)) in filled:
                loc+=1
            else:
                break
        offset_locs.append(ceil(loc/2.0)*((-1)**(loc % 2)))
    return offset_locs


def plot_paths(path_sets, offset_size=6):
    colors = tuple(path_sets.keys())
    shape = (path_sets[colors[0]][0].count('E'), path_sets[colors[0]][0].count('N'))
    size = sum([len(path_sets[c]) for c in colors])
    padding = ceil(offset_size/1.5*size)
    fig, ax = plt.subplots()
    ax.set_xlim(-1*padding, 5*padding*shape[0]+padding)
    ax.set_ylim(-1*padding, 5*padding*shape[1]+padding)

    # Draw the grid lines
    for i in range(0, 5*padding*shape[0], 5*padding):
        for j in range(0, 5*padding*shape[1]+1, 5*padding):
            path = Path(((i, j), (i+5*padding, j)), (Path.MOVETO, Path.LINETO))
            patch = patches.PathPatch(path, lw=1,color='black')
            ax.add_patch(patch)
    for i in range(0, 5*padding*shape[1], 5*padding):
        for j in range(0, 5*padding*shape[0]+1, 5*padding):
            path = Path(((j, i), (j, i+5*padding)), (Path.MOVETO, Path.LINETO))
            patch = patches.PathPatch(path, lw=1,color='black')
            ax.add_patch(patch)

    all_edges = []
    for a in range(shape[0]):
        for b in range(shape[1]+1):
            all_edges.append((a,b,a+1,b))
    for b in range(shape[1]):
        for a in range(shape[0]+1):
            all_edges.append((a,b,a,b+1))
    edges_filled = {x:[] for x in all_edges}
    del all_edges
    for color in colors:
        for p in path_sets[color]:
            p_ints = path_to_ints(p)
            edges = list(lp.Edges(p))
            offsets = offset_location_list(p_ints,edges_filled,edges)
            offsets.append(0)
            print(edges)
            print(edges_filled)
            print(offsets)
            loc = [0+offset_size*(p[0] == 'N')*offsets[0],
                   0+offset_size*(p[0] == 'E')*offsets[0]]
            cumulative = 0
            for j, x in enumerate(p_ints):
                old_loc = loc.copy()
                if x > 0:
                    loc[0] += 5*padding*x-offset_size*offsets[j+1]#+offset_size*offsets[j]
                    print(j, offsets[j+1])
                else:
                    loc[1] += 5*padding*abs(x)-offset_size*offsets[j+1]#+offset_size*offsets[j]
                    print(j, offsets[j+1])
                path = Path((old_loc, loc), (Path.MOVETO, Path.LINETO))
                patch = patches.PathPatch(path, lw=1.5, color=color)
                ax.add_patch(patch)
                for e in edges[cumulative:cumulative+abs(x)]:
                    edges_filled[e].append(offsets[j])
                cumulative+=abs(x)

    plt.axis('off')
    plt.show()




plot_paths(paths)
