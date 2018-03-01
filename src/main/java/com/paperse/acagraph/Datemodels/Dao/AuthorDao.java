package com.paperse.acagraph.Datemodels.Dao;

import com.paperse.acagraph.Datemodels.domain.Author;
import org.springframework.data.repository.CrudRepository;

/**
 * Created by sunhaoran on 2018/3/1.
 */
public interface AuthorDao extends CrudRepository<Author, String> {
}
