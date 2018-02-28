package com.paperse.acagraph.Datemodels.Dao;

import com.paperse.acagraph.Datemodels.domain.Paper;
import org.springframework.data.repository.CrudRepository;

import java.util.List;

/**
 * Created by sunhaoran on 2017/7/19.
 */
public interface TangoUserDao extends CrudRepository<Paper, String> {
    public Paper findByIdAndValid(String id, boolean valid);
    public List<Paper> findByRegDateAndValid(String date, boolean valid);
    public List<Paper> findByValid(boolean valid);
}
