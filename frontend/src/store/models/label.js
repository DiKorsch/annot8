let rank_orders = {
  "order": 0,
  "family": 1,
  "genus": 2,
  "species": 3,
}

export default class File {
  constructor(data) {
    this.id = data.id;
    this.name = data.name;
    this.kr_nr = data.kr_nr;
    this.rank = data.taxonomic_rank;
    this.rank_order = rank_orders[this.rank];
    this.parent_id = data.parent_id;
    this.parent = undefined;
    this.children = [];

  }

  add_child(child){
    this.children.push(child);
  }

  set_parent(parent){
    this.parent = parent;
  }

  contains(search_term){
    return this.name.toLowerCase().includes(search_term) || `${this.kr_nr}`.includes(search_term)
  }
}
