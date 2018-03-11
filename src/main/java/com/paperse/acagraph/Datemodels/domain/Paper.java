package com.paperse.acagraph.Datemodels.domain;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.validation.constraints.NotNull;

/**
 * Created by sunhaoran on 2017/7/19.
 */
@Entity
public class Paper {
    @Id
    @NotNull
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    //原id
    private String oriid;

    //标题
    private String title;

    //作者
    private String authors;

    //会议
    private String vuene;

    //发布年份
    private int year;

    //关键字
    private String keywords;

    //fos
    private String fos;

    //被引数
    private int ncite;

    //参考文献
    private String refs;

    //类型
    private String doctype;

    //出版商
    private String publisher;

    //isbn
    private String isbn;

    //pdf
    private String pdf;

    //url
    private String url;

    //摘要
    private String abs;

    //作者id
    private String authorsid;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getOriid() {
        return oriid;
    }

    public void setOriid(String oriid) {
        this.oriid = oriid;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getAuthors() {
        return authors;
    }

    public void setAuthors(String authors) {
        this.authors = authors;
    }

    public int getYear() {
        return year;
    }

    public void setYear(int year) {
        this.year = year;
    }

    public String getKeywords() {
        return keywords;
    }

    public void setKeywords(String keywords) {
        this.keywords = keywords;
    }

    public String getFos() {
        return fos;
    }

    public void setFos(String fos) {
        this.fos = fos;
    }

    public int getNcite() {
        return ncite;
    }

    public void setNcite(int ncite) {
        this.ncite = ncite;
    }

    public String getRefs() {
        return refs;
    }

    public void setRefs(String refs) {
        this.refs = refs;
    }

    public String getDoctype() {
        return doctype;
    }

    public void setDoctype(String doctype) {
        this.doctype = doctype;
    }

    public String getPublisher() {
        return publisher;
    }

    public void setPublisher(String publisher) {
        this.publisher = publisher;
    }

    public String getIsbn() {
        return isbn;
    }

    public void setIsbn(String isbn) {
        this.isbn = isbn;
    }

    public String getPdf() {
        return pdf;
    }

    public void setPdf(String pdf) {
        this.pdf = pdf;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getAbs() {
        return abs;
    }

    public void setAbs(String abs) {
        this.abs = abs;
    }

    public String getVuene() {
        return vuene;
    }

    public void setVuene(String vuene) {
        this.vuene = vuene;
    }

    public String getAuthorsid() {
        return authorsid;
    }

    public void setAuthorsid(String authorsid) {
        this.authorsid = authorsid;
    }
}
