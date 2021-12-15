import graphviz

def save_graph_as_svg(dtc, X_train, X_predict,  output_file_name, directory = './'):
    left_children = dtc.tree_.children_left
    right_children = dtc.tree_.children_right
    node_num = dtc.tree_.node_count
    threshold = dtc.tree_.threshold.astype(int)

    node_indicator = dtc.decision_path([X_predict])

    sample_id = 0
    # obtain ids of the nodes `sample_id` goes through, i.e., row `sample_id`
    node_index = node_indicator.indices[
        node_indicator.indptr[sample_id] : node_indicator.indptr[sample_id + 1]
    ]

    node = ''
    leaf_node = []
    for n in range(node_num):
        if threshold[n] >= 0:
            node += str(n) + f' [label="{X_train.columns[dtc.tree_.feature[n]]}<={threshold[n]}" shape=box '
            if n in node_index:
                node += 'style="filled"];'
            else :
                node += "];"
        else :
            leaf_node+=[n]
            if dtc.tree_.value[n].squeeze().argmax():
                node += f'{n} [label="30up\n{int(dtc.tree_.value[n].squeeze().max()/sum(dtc.tree_.value[n].squeeze())*100)}%" '
            else :
                node += f'{n} [label="30down\n{int(dtc.tree_.value[n].squeeze().max()/sum(dtc.tree_.value[n].squeeze())*100)}%" shape=box style="filled" fillcolor="yellow"'
                
            if n in node_index:
                node += 'style="filled"];'
            else :
                node += "];"

    max_path = (0, 0) # node, percent
    edge = ''
    for _node in range(node_num):
        if left_children[_node] >= 0:
            edge += f"{_node}--{left_children[_node]}"
            if left_children[_node] in node_index:
                edge += " [color=red penwidth=5];"
                cur_node = left_children[_node]
                if (left_children[cur_node] in leaf_node) & (max_path[1] < int(dtc.tree_.value[left_children[cur_node]].squeeze().max()/sum(dtc.tree_.value[left_children[cur_node]].squeeze())*100)):
                    print(left_children[cur_node], int(dtc.tree_.value[left_children[cur_node]].squeeze().max()/sum(dtc.tree_.value[left_children[cur_node]].squeeze())*100))
                    max_path = ([cur_node, left_children[cur_node]], int(dtc.tree_.value[left_children[cur_node]].squeeze().max()/sum(dtc.tree_.value[left_children[cur_node]].squeeze())*100))
                    
                if (right_children[cur_node] in leaf_node) & (max_path[1] < int(dtc.tree_.value[right_children[cur_node]].squeeze().max()/sum(dtc.tree_.value[right_children[cur_node]].squeeze())*100)):
                    print(right_children[cur_node], int(dtc.tree_.value[right_children[cur_node]].squeeze().max()/sum(dtc.tree_.value[right_children[cur_node]].squeeze())*100))
                    max_path = ([cur_node, right_children[cur_node]], int(dtc.tree_.value[right_children[cur_node]].squeeze().max()/sum(dtc.tree_.value[right_children[cur_node]].squeeze())*100))
            else :
                edge += " [style=dotted];"
            
                
                
        if right_children[_node] >= 0:
            edge += f"{_node}--{right_children[_node]}"
            if right_children[_node] in node_index:
                edge += " [color=red penwidth=5];"
                cur_node = right_children[_node]
                if (left_children[cur_node] in leaf_node) & (max_path[1] < int(dtc.tree_.value[left_children[cur_node]].squeeze().max()/sum(dtc.tree_.value[left_children[cur_node]].squeeze())*100)):
                    print(left_children[cur_node], int(dtc.tree_.value[left_children[cur_node]].squeeze().max()/sum(dtc.tree_.value[left_children[cur_node]].squeeze())*100))
                    max_path = ([cur_node,left_children[cur_node]], int(dtc.tree_.value[left_children[cur_node]].squeeze().max()/sum(dtc.tree_.value[left_children[cur_node]].squeeze())*100))
                    
                if (right_children[cur_node] in leaf_node) & (max_path[1] < int(dtc.tree_.value[right_children[cur_node]].squeeze().max()/sum(dtc.tree_.value[right_children[cur_node]].squeeze())*100)):
                    print(right_children[cur_node], int(dtc.tree_.value[right_children[cur_node]].squeeze().max()/sum(dtc.tree_.value[right_children[cur_node]].squeeze())*100))
                    max_path = ([cur_node,right_children[cur_node]], int(dtc.tree_.value[right_children[cur_node]].squeeze().max()/sum(dtc.tree_.value[right_children[cur_node]].squeeze())*100))
            else :
                edge += " [style=dotted];"
            
    edge += f"{max_path[0][0]} -- {max_path[0][1]} [color=green penwidth=5];"

    dot_string = f"""
    graph graphname {{
        {node}
        {edge}
    }}
    """
    

    if type(dot_string) is str:
        g = graphviz.Source(dot_string)
    elif isinstance(dot_string, (graphviz.dot.Digraph, graphviz.dot.Graph)):
        g = dot_string
    g.format='png'
    g.filename = output_file_name
    g.directory = './'
    g.render(view=False)
    return g