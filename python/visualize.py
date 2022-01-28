import os
from math import ceil
from io import BytesIO
import ast
import base64
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib import patches
import lattice_paths as lp

#set1 = set(('EEEENNN', 'EENENNE', 'ENENEEN', 'ENNENEE', 'NEEEENN', 'NNEEENE'))
#set2 = set(('EEEENNN', 'EENENNE', 'ENENNEE', 'ENNEEEN', 'NEEEENN', 'NENNEEE', 'NNEEENE'))
#s1 = sorted(list(set1.difference(set2)))
#s2 = sorted(list(set2.difference(set1)))
#s3 = sorted(list(set1.intersection(set2)))
#paths = {'green': tuple(s3), 'blue': tuple(s1), 'orange': tuple(s2)}

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

def get_all_lattice_edges(shape):
    all_edges = []
    for a in range(shape[0]):
        for b in range(shape[1]+1):
            all_edges.append((a,b,a+1,b))
    for b in range(shape[1]):
        for a in range(shape[0]+1):
            all_edges.append((a,b,a,b+1))
    return all_edges

def plot_paths(path_sets, offset_size=6, scale_factor=5):
    colors = tuple(path_sets.keys())
    shape = (path_sets[colors[0]][0].count('E'), path_sets[colors[0]][0].count('N'))
    size = sum([len(path_sets[c]) for c in colors])
    padding = ceil(offset_size/1.5*size)
    fig, ax = plt.subplots()
    ax.set_xlim(-1*padding, scale_factor*padding*shape[0]+padding)
    ax.set_ylim(-1*padding, scale_factor*padding*shape[1]+padding)

    # Draw the grid lines
    for i in range(0, scale_factor*padding*shape[0], scale_factor*padding):
        for j in range(0, scale_factor*padding*shape[1]+1, scale_factor*padding):
            path = Path(((i, j), (i+scale_factor*padding, j)), (Path.MOVETO, Path.LINETO))
            patch = patches.PathPatch(path, lw=1,color='black')
            ax.add_patch(patch)
    for i in range(0, scale_factor*padding*shape[1], scale_factor*padding):
        for j in range(0, scale_factor*padding*shape[0]+1, scale_factor*padding):
            path = Path(((j, i), (j, i+scale_factor*padding)), (Path.MOVETO, Path.LINETO))
            patch = patches.PathPatch(path, lw=1,color='black')
            ax.add_patch(patch)

    edges_filled = {x:[] for x in get_all_lattice_edges(shape)}
    for color in colors:
        for p in path_sets[color]:
            p_ints = path_to_ints(p)
            edges = list(lp.Edges(p))
            offsets = offset_location_list(p_ints, edges_filled, edges)
            offsets.append(0)
            cumulative = 0
            path_points = [[0,0]]
            for x in p_ints:
                point_ = edges[cumulative+abs(x)-1][2:4]
                path_points.append([point_[0]*scale_factor*padding, point_[1]*scale_factor*padding])
                cumulative += abs(x)
            for i, point in enumerate(path_points[1:]):
                if p_ints[i] > 0:
                    path_points[i][1] += offset_size*offsets[i]
                    path_points[i+1][1] += offset_size*offsets[i]
                elif p_ints[i] < 0:
                    path_points[i][0] += offset_size*offsets[i]
                    path_points[i+1][0] += offset_size*offsets[i]
            path = Path(path_points,None)
            patch = patches.PathPatch(path, lw=1.5, color=color, fill=False)
            ax.add_patch(patch)
            cumulative = 0
            for j, x in enumerate(p_ints):
                for e in edges[cumulative:cumulative+abs(x)]:
                    edges_filled[e].append(offsets[j])
                cumulative+=abs(x)

    return_file = BytesIO()
    plt.axis('off')
    fig.savefig(return_file, format='svg')
    soup = BeautifulSoup(return_file.getvalue().decode('utf-8'), 'html.parser')
    return str(soup.svg)

def two_path_sets_svg(set1, set2, colors=('green','blue','orange')):
    set1 = set(set1)
    set2 = set(set2)
    s1 = sorted(list(set1.difference(set2)))
    s2 = sorted(list(set2.difference(set1)))
    s3 = sorted(list(set1.intersection(set2)))
    if len(s3):
        paths = {colors[0]: tuple(s3), colors[1]: tuple(s1), colors[2]: tuple(s2)}
    else:
        paths = {colors[1]: tuple(s1), colors[2]: tuple(s2)}
    return plot_paths(paths)

def create_report(data_file, save_file):
    data = pd.read_csv(data_file,sep='\t')
    data['greedy_set'] = [ast.literal_eval(x) for x in data['greedy_set']]
    data['max_sets'] = [ast.literal_eval(x) for x in data['max_sets']]
    title = f"<h1>Data for <i>k</i>-distinct paths on the {data.m[0]} by {data.n[0]} lattice</h1>"
    first_table = data[['m', 'n', 'k', 'greedy_cardinality', 'max_cardinality']]
    first_table.rename({'m':'M', 'n':'N', 'k':'K', 'greedy_cardinality':'Greedy Cardinality', 'max_cardinality':'Maximum Cardinality'})
    first_table.to_html('temp.html',index=False)
    with open('temp.html', 'r') as f:
        first_table = f.read()
    os.system("rm temp.html")
    table = str(BeautifulSoup(first_table, 'html.parser'))
    table_description = "<p>Below is a table giving the cardinality of the sets returned by the greedy algorithm and a brute force search.</p>"
    data_html = []
    for i, row in data.iterrows():
        data_html.append(f"<h2>{row['k']}-Distinct Sets</h2>")
        if row['greedy_is_max']:
            data_html.append("<p>In this case, the greedy algorithm gives a maximum cardinality set.</p>")
            data_html.append(f"<p>The greedy set is visualized below. The paths are {row['greedy_set']}.</p>")
            data_html.append(plot_paths({'red': row['greedy_set']}))
            data_html.append("<p>Other maximum sets include:</p><ul>")
            for set_ in row['max_sets']:
                data_html.append(f"<li>{set_}</li>")
            data_html.append("</ul>")
        else:
            data_html.append("<p>In this case, the greedy algorithm does not give a maximum cardinality set.</p>")
            data_html.append(f"<p>The greedy set is visualized below. The paths are {row['greedy_set']}.</p>")
            data_html.append(plot_paths({'red': row['greedy_set']}))
            data_html.append("<p>Below, we compare the greedy set to each maximum sets, with similar paths paired together and differences in bold.</p>")
            for set_ in row['max_sets']:
                data_html.append(highlight_diffs(match(row['greedy_set'],set_))+"<br> <br>")
            data_html.append("<p>Below, we compare the greedy set to maximum sets on lattices. Shared paths are green, paths from only the greedy set are blue, and paths from a maximum set are orange.</p>")
            for set_ in row['max_sets']:
                data_html.append(f"<h4>{set_}</h4>")
                data_html.append(f"{two_path_sets_svg(row['greedy_set'],set_)}")

    html = f"{title}{table_description}{table}"
    html = html + "\n".join(data_html)

    with open(save_file+'.html','w') as f:
        f.write(html)

def find_diffs(path1, path2):
    # identify places where strings differ
    diffs = []
    for i, c in enumerate(path1):
        if c != path2[i]:
            diffs.append(i)
    return tuple(diffs)


def swap_distance(path1, path2):
    swaps = 0
    diffs = find_diffs(path1, path2)
    while len(diffs) > 0:
        spot = max(diffs)
        char_needed = path1[spot]
        nearest = spot - path2[spot::-1].find(char_needed)
        swaps += spot - nearest
        path2 = path2[:nearest] + path2[spot] + path2[nearest + 1:spot] + \
                char_needed + path2[spot + 1:]
        diffs = find_diffs(path1, path2)
    return swaps

def match(set1, set2):
    if len(set1)>len(set2):
        set1, set2 = set2, set1
    pairs = {}
    distances = {}
    for i, path1 in enumerate(set1):
        distances[i] = {}
        for j, path2 in enumerate(set2):
            if j in pairs.values():
                continue
            d = swap_distance(path1, path2)
            if d == 0:
                pairs[i] = j
                distances.pop(i, None)
                for key in distances:
                    distances[key].pop(j, None)
                break
            distances[i][j] = d
    # match non zero distances
    while len(distances):
        updates = 0
        closest = min([x for y in distances.values() for x in y.values()])
        for path in tuple(distances.keys()):
            if list(distances[path].values()).count(closest) == 1:
                for p in distances[path]:
                    if distances[path][p]==closest:
                        pairs[path] = p
                        break
                for key in distances:
                    distances[key].pop(pairs[path], None)
                distances.pop(path, None)
        if not updates:
            for path in tuple(distances.keys()):
                if list(distances[path].values()).count(closest) > 1:
                    for p in distances[path]:
                        if distances[path][p]==closest:
                            pairs[path] = p
                            break
                    for key in distances:
                        distances[key].pop(pairs[path], None)
                    distances.pop(path, None)
    comparison = ""
    for p1 in pairs:
        comparison += set1[p1] + ' ' + set2[pairs[p1]] + "\n"
    missing = int((len(set2)*(len(set2)-1))/2 - sum(pairs.values()))
    comparison += ' '*(len(set1[0])+1) + set2[missing]
    return comparison

def highlight_diffs(comparison):
    pairs = comparison.split('\n')
    new_string = '<table>'
    for pair in pairs:
        if pair[0]==' ':
            new_string += "<tr><td></td><td>" + pair.split(' ')[-1] + "</td></tr>"
        elif pair.split(' ')[0] == pair.split(' ')[1]:
            new_string += "<tr><td>" + pair.split(' ')[0] + "</td><td>" + pair.split(' ')[1] + "</td></tr>"
        else:
            paths = pair.split(' ')
            new_paths = ['','']
            for i, c in enumerate(paths[0]):
                if c!=paths[1][i]:
                    new_paths[0]+="<b>"+c+"</b>"
                    new_paths[1]+="<b>"+paths[1][i]+"</b>"
                else:
                    new_paths[0]+=c
                    new_paths[1]+=paths[1][i]
            new_string += "<tr><td>" + new_paths[0] + "</td><td>" + new_paths[1] + "</td></tr>"
    return new_string + '</table>'