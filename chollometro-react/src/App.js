// import logo from './logo.svg';
import './App.css';
import {ReactiveBase, SearchBox, MultiList, ReactiveList, TreeList, RangeSlider} from "@appbaseio/reactivesearch";

function App() {

  return (
      <ReactiveBase
          app="scrapy"
          url="http://localhost:9200"
          // enableAppbase
          theme={{
            typography: {
              fontFamily:
                  '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Noto Sans", "Ubuntu", "Droid Sans", "Helvetica Neue", sans-serif',
              fontSize: "16px",
            },
            colors: {
              backgroundColor: "#212121",
              primaryTextColor: "#fff",
              primaryColor: "#2196F3",
              titleColor: "#fff",
              alertColor: "#d9534f",
              borderColor: "#666",
            },
          }}
      >
        <MultiList
            componentId="Category"
            dataField="categories"
            style={{
              marginBottom: 20
            }}
            title="Categories"
            className='categories'
            // size={20}
            sortBy='count'
            queryFormat='or'
            selectAllLabel='All Categories'
            showCheckbox={true}
            showCount={true}
            showSearch={true}
            placeholder='Search for a category'
            react={{
              and: [
                "Seller",
                "Prices",
              ],
            }}
            showFilter={true}
            filterLabel='Categories'
            URLParams={false}
            innerClass={{
              label: "title",
              input: "input",

            }}
            style={{
              padding: '5px',
              width: '20%',
            }}


        />
        <MultiList
            componentId="Seller"
            dataField="seller"
            style={{
              marginBottom: 20
            }}
            title="Sellers"
            className='sellers'
            // size={20}
            sortBy='count'
            queryFormat='or'
            selectAllLabel='All sellers'
            showCheckbox={true}
            showCount={true}
            showSearch={true}
            placeholder='Search for a seller'
            react={{
              and: [
                "Category",
                "Prices",
              ],
            }}
            showFilter={true}
            filterLabel='Seller'
            URLParams={false}
            innerClass={{
              label: "list-item",
              input: "list-input",
            }}
            style={{
              padding: '5px',
              width: '20%',
            }}
        />
        <RangeSlider
            title={"Price Range"}
            componentId='Prices'
            dataField='price'
            className='prices'
            tooltipTrigger='hover'
            range={{
              start: 0,
              end: 4000,
            }}
            rangeLabels={{
              start: "0",
              end: "4000",
            }}
            react={{
              and: [
                "Category",
                "Seller",
              ],
            }}
            showHistogram
            style={{
              padding: '5px',
              width: '20%',
            }}
        />
        <ReactiveList
            componentId="results"
            react={{
              and: [
                "Category",
                "Seller",
                "Prices",
              ],
            }}
            dataField={[
              { field: "article.keyword", weight: 3 },
              { field: "url.keyword", weight: 2 },
              { field: "price", weight: 1 },
            ]}
            // renderItem={res =>
            //     <div>
            //       {res.article}
            //       {res.url}
            //       {res.price}
            //     </div>}
            // print dataField
            renderItem={res => (
                <div className="result-card">

                  <div className="info-container">
                    <div className="info">
                      <div className="title">
                          <a href={res
                            .url} target="_blank" rel="noopener noreferrer">
                          <img src={res.image} alt={res.article}/>
                          </a>
                          <br/>
                          <a href={res
                            .url} target="_blank" rel="noopener noreferrer">
                            <b id={"article"}>{res.article}</b>
                          </a>
                      </div>
                      <div className="price">${res.price}</div>
                    </div>
                  </div>
                  <br/>
                </div>
            )}

            sortOptions={[
              {
                dataField: "price",
                sortBy: "asc",
                label: "Lowest Price",
              },
              {
                dataField: "price",
                sortBy: "desc",
                label: "Highest Price",
              },
            ]}

            style={{
              padding: '5px',
              width: '60%',
              position: 'absolute',
            }}
            pagination={true}
            paginationAt='bottom'
        />
        {/*<ReactiveList*/}
        {/*    defaultQuery={() => ({ track_total_hits: true })}*/}
        {/*    componentId='results'*/}
        {/*    dataField={[*/}
        {/*      { field: "article.keyword", weight: 3 },*/}
        {/*      { field: "url.keyword", weight: 2 },*/}
        {/*    ]}*/}
        {/*    react={{*/}
        {/*      and: [*/}
        {/*        "Category",*/}
        {/*        "Seller",*/}
        {/*        "Prices",*/}
        {/*      ],*/}
        {/*    }}*/}
        {/*    pagination={true}*/}
        {/*    className='Result_card'*/}
        {/*    paginationAt='bottom'*/}
        {/*    pages={5}*/}
        {/*    size={12}*/}
        {/*    Loader='Loading...'*/}
        {/*    noResults='No results were found...'*/}
        {/*    // sortOptions={[*/}
        {/*    //   {*/}
        {/*    //     dataField: "vote_count",*/}
        {/*    //     sortBy: "desc",*/}
        {/*    //     label: "Sort by vote-count(High to Low) \u00A0",*/}
        {/*    //   },*/}
        {/*    //   {*/}
        {/*    //     dataField: "popularity",*/}
        {/*    //     sortBy: "desc",*/}
        {/*    //     label: "Sort by Popularity(High to Low)\u00A0 \u00A0",*/}
        {/*    //   },*/}
        {/*    //   {*/}
        {/*    //     dataField: "vote_average",*/}
        {/*    //     sortBy: "desc",*/}
        {/*    //     label: "Sort by Ratings(High to Low) \u00A0",*/}
        {/*    //   },*/}
        {/*    //   {*/}
        {/*    //     dataField: "original_title.raw",*/}
        {/*    //     sortBy: "asc",*/}
        {/*    //     label: "Sort by Title(A-Z) \u00A0",*/}
        {/*    //   },*/}
        {/*    // ]}*/}
        {/*    innerClass={{*/}
        {/*      title: "result-title",*/}
        {/*      listItem: "result-item",*/}
        {/*      list: "list-container",*/}
        {/*      sortOptions: "sort-options",*/}
        {/*      resultStats: "result-stats",*/}
        {/*      resultsInfo: "result-list-info",*/}
        {/*      poweredBy: "powered-by",*/}
        {/*    }}*/}
        {/*>*/}
        {/*  {({ data }) => (*/}
        {/*      <ReactiveList.ResultCardsWrapper style={{ margin: "8px 0 0" }}>*/}
        {/*        {data.map((item) => (*/}
        {/*            <div style={{ marginRight: "15px" }} className='main-description'>*/}
        {/*              <div className='ih-item square effect6 top_to_bottom'>*/}
        {/*                <a*/}
        {/*                    target='#'*/}
        {/*                    href={item.url}*/}
        {/*                >*/}
        {/*                  /!*<div className='img'>*!/*/}
        {/*                  /!*  <img*!/*/}
        {/*                  /!*      src={item.poster_path}*!/*/}
        {/*                  /!*      alt={item.original_title}*!/*/}
        {/*                  /!*      className='result-image'*!/*/}
        {/*                  /!*  />*!/*/}
        {/*                  /!*</div>*!/*/}

        {/*                  <div className='info colored'>*/}
        {/*                    <h3 className='overlay-title'>{item.article}</h3>*/}
        {/*                    <div className='overlay-description'>{item.description}</div>*/}
        {/*                  </div>*/}
        {/*                </a>*/}
        {/*              </div>*/}
        {/*            </div>*/}
        {/*        ))}*/}
        {/*      </ReactiveList.ResultCardsWrapper>*/}
        {/*  )}*/}
        {/*</ReactiveList>*/}
      </ReactiveBase>

  );
}


export default App;
