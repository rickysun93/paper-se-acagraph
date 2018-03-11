package com.paperse.acagraph.Datemodels.Dao;

import com.paperse.acagraph.Datemodels.domain.Paper;
import org.springframework.data.repository.PagingAndSortingRepository;

/**
 * Created by sunhaoran on 2017/7/19.
 */
public interface PaperDao extends PagingAndSortingRepository<Paper, String> {
}
