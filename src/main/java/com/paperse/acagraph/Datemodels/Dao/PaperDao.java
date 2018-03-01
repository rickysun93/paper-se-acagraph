package com.paperse.acagraph.Datemodels.Dao;

import com.paperse.acagraph.Datemodels.domain.Paper;
import org.springframework.data.repository.CrudRepository;

/**
 * Created by sunhaoran on 2017/7/19.
 */
public interface PaperDao extends CrudRepository<Paper, String> {
}
