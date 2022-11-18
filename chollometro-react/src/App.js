// import logo from './logo.svg';
import './App.css';
import {ReactiveBase,MultiList,ReactiveList,RangeSlider,DataSearch} from "@appbaseio/reactivesearch";

function App() {
  return (
      <ReactiveBase
          app="scrapy"
          url="http://localhost:9200"
          theme={{
            typography: {
              fontFamily:
                  '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Noto Sans", "Ubuntu", "Droid Sans", "Helvetica Neue", sans-serif',
              fontSize: "16px"
            }
          }}
      >
        <div className="flexFirstRow">
          <div className="flexBoxColumn">
            <DataSearch
                componentId="Search"
                dataField={["article","description"]}
                fieldWeights={[3, 1]}
                mode="select" // accepts either of 'select' or 'tag' defaults to 'select'
                title="Search"
                placeholder="Search for products"
                autosuggest={false}
                // highlight={true}
                // queryFormat="and"
                fuzziness="AUTO"
                debounce={1000}
                react={{
                  and: [
                    "Seller",
                    "Prices",
                    "Category",
                  ],
                }}
                size={0}
                showFilter={true}
                style={{
                  padding: '5px',
                  paddingRight: '10px',
                  width: '100%',
                }}
            />
            <MultiList
                componentId="Category"
                dataField="categories"
                style={{
                  marginBottom: 20
                }}
                title="Categories"
                className='categories'
                size={100}
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
                    "Search",
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
                  paddingRight: '10px',
                  width: '100%',
                }}
            />
            <MultiList
                componentId="Seller"
                dataField="seller"
                style={{
                  marginBottom: 20
                }}
                size={100}
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
                    "Search",
                  ],
                }}
                showFilter={true}
                filterLabel='Seller'
                URLParams={false}
                innerClass={{
                  label: "item",
                  input: "input",
                }}
                style={{
                  padding: '5px',
                  paddingRight: '10px',
                  width: '100%',
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
                  end: 3000,
                }}
                rangeLabels={{
                  start: "0",
                  end: "3000",
                }}
                react={{
                  and: [
                    "Category",
                    "Seller",
                    "Search",
                  ],
                }}
                showHistogram
                style={{
                  padding: '5px',
                  width: '100%',
                  paddingRight: '10px'
                }}
                innerClass={
                  {
                    slider: 'slider',
                  }
                }
            />
          </div>
          <div className="todo">
            <ReactiveList
                componentId="results"
                react={{
                  and: [
                    "Category",
                    "Seller",
                    "Prices",
                    "Search",
                  ],
                }}
                dataField={[
                  { field: "article.keyword", weight: 3 },
                  { field: "price", weight: 1 },
                ]}
                size={24}
                innerClass={{
                  list: "list"
                }}
                renderItem={res => (
                    <div className="result-card">
                      <div className="info-container">
                        <div className="info">
                          <div className="title">
                            <div className="image">
                              <a href={res
                                  .url} target="_blank" rel="noopener noreferrer">
                                <img src={res.image} alt={res.article}/>
                              </a>
                            </div>
                            <br/>
                            <a href={res
                                .url} target="_blank" rel="noopener noreferrer">
                              <b className="article-text" id={"article"}>{res.article}</b>
                            </a>
                          </div>
                          <div className="price">{res.price}€</div>
                        </div>
                      </div>
                      <br/>
                    </div>
                )}

                sortOptions={[
                  {
                    dataField: "_score",
                    sortBy: "desc",
                    label: "Relevance",
                  },
                  {
                    dataField: "price",
                    sortBy: "asc",
                    label: "Lowest Price",
                  },
                  {
                    dataField: "price",
                    sortBy: "desc",
                    label: "Highest Price",
                  }
                ]}
                style={{
                  padding: '5px',
                  width: '80%',
                  position: 'absolute',
                }}
                pagination={true}
                paginationAt='bottom'
            />
          </div>
        </div>
      </ReactiveBase>
  );
}


export default App;
