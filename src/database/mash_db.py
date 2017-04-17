from base import BaseDB

class MashDB(BaseDB):

  def save_sample_result(self, sample_id, highest_match=None):
    if highest_match:
      query = "insert into sample_result (sample_id, highest_match) values (%s, %s) returning id"
      ret_id = self.insert(query, (sample_id, highest_match))
    else:
      query = "insert into sample_result (sample_id) values (%s) returning id"
      ret_id = self.insert(query, (sample_id,))
    return ret_id
  
  def save_mash_output(self, sample_id, output_rows):
    query = "insert into mash_output (sample_result_id, reference_id, query_id, mash_distance, p_value, matching_hashes) values "

    # Remove empty row
    for idx, row in enumerate(output_rows):
       if len(row) != 5:
        output_rows.pop(idx)

    # Build big query arguments
    query_args = ','.join(self.cur.mogrify("({}, %s,%s,%s,%s,%s)".format(sample_id), row) for row in output_rows)

    self.cur.execute(query + query_args)
    self.conn.commit()

  def update_sample_result(self, id, highest_match):
    query = "update sample_result set highest_match = %s where id = %s"
    self.update(query, (highest_match, id))
  
  def get_top_n_mash_results(self, sample_id, n=10):
    query = "select * from mash_output where sample_result_id = %s order by mash_distance limit %s"
    top_n = self.get(query, (sample_id, n))
    return top_n

  def get_sample_by_id(self, sample_id):
    query = "select * from sample_result where sample_id = %s"
    sample = self.get(query, (sample_id,))
    return sample