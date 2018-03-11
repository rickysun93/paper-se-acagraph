package com.paperse.acagraph.Datemodels.Dao;

import com.paperse.acagraph.Datemodels.domain.Author;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * Created by sunhaoran on 2018/3/1.
 */
public interface AuthorDao extends JpaRepository<Author, String> {
    public Author findByNamelower(String nl);
}
