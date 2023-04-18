'use strict';

var MongoClient = require('mongodb').MongoClient;
const url = process.env.DB;

const connectToCluster = async () => {
  let mongoClient;

  try {
    mongoClient = new MongoClient(url);
    await mongoClient.connect();
    return mongoClient;
  } catch (error) {
    // process.exit();
  }
}

const insertLikes = async (symbol, likes, ip) => {
  let mongoClient;
  try {
    mongoClient = await connectToCluster();
    const db = mongoClient.db('stockprices');
    const collection = db.collection('likes');
    const query = { symbol };
    const update = { $set: { likes }, $addToSet: { ips: ip } };
    const options = { upsert: true };
    await collection.updateOne(query, update, options);
    return ;
  } catch (error) {
    console.log(error)
    return ;
  }finally {
    await mongoClient.close();
  }
}

const findCurrency = async (symbol, ip) => {
  let mongoClient;
  try {
    mongoClient = await connectToCluster();
    const db = mongoClient.db('stockprices');
    const collection = db.collection('likes');
    const query = (ip) ? { symbol, ips: { $eq: ip } } : { symbol };
    return await collection.find(query).toArray();
  } catch (error) {
    return [];
  }finally {
    await mongoClient.close();
  }
}

const getLikes = async (symbol, ip = null) => {
  return (await findCurrency(symbol, ip))[0]?.likes || 0;
}

const getStock = async (symbol) => {
  const url = `https://stock-price-checker-proxy.freecodecamp.rocks/v1/stock/${symbol}/quote`;
  const res =  await fetch(url);
  return res.json();
}

module.exports = function (app) {

  app.route('/api/stock-prices')
    .get(async function (req, res) {
      const { stock } = req.query;
      const { like } = req.query;
      const ip = req.ip;
      if (stock) {
        if (Array.isArray(stock) && stock.length > 1) {
          const dataStock1 = await getStock(stock[0]);
          const dataStock2 = await getStock(stock[1]);
          const userLikesStock1 = await getLikes(dataStock1.symbol, ip);
          const userLikesStock2 = await getLikes(dataStock2.symbol, ip);
          const totalLikesStock1 = await getLikes(dataStock1.symbol);
          const totalLikesStock2 = await getLikes(dataStock2.symbol);

          const diffLikesStock1 = totalLikesStock1 - totalLikesStock2;
          const diffLikesStock2 = totalLikesStock2 - totalLikesStock1;

          if (like && (!userLikesStock1 || !userLikesStock2)) {
            await insertLikes(dataStock1.symbol, totalLikesStock1 + 1, ip);
            await insertLikes(dataStock2.symbol, totalLikesStock2 + 1, ip);
          }

          res.json({
            "stockData": [
              {
                "stock": dataStock1.symbol,
                "price": dataStock1.latestPrice,
                "rel_likes": diffLikesStock1
              },
              {
                "stock": dataStock2.symbol,
                "price": dataStock2.latestPrice,
                "rel_likes": diffLikesStock2
              }
            ]
          });
        } else {
          const dataStock = await getStock(stock);
          const userLikes = await getLikes(dataStock.symbol, ip);
          let likes = await getLikes(dataStock.symbol);
          if (like && !userLikes) {
            await insertLikes(dataStock.symbol, likes + 1, ip);
            likes = likes + 1;
          }
          return res.json({
            "stockData": {
              "stock": dataStock.symbol,
              "price": dataStock.latestPrice,
              "likes": likes
            }
          });
          }
        }      
    });
};
