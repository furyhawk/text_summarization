import axios from './axios';

export default function getData(url) {
  return axios.get(url)
    .then(response => {
      if (response.statusText !== "OK") {
        throw Error("There was a problem fetching data.");
      }

      return response.data

    });
}

export function getAllModels() {
  return getData("/models");
}

export function postPrediction(path, prediction) {
  return axios.post(path, prediction).then(response => {
      if (response.statusText !== "OK") {
        throw Error("There was a problem fetching data.");
      }

      return response.data
    });
}



// export function getBookings (bookableId, startDate, endDate) {

//   const start = shortISO(startDate);
//   const end = shortISO(endDate);

//   const urlRoot = "http://localhost:3001/bookings";

//   const query = `bookableId=${bookableId}` +
//     `&date_gte=${start}&date_lte=${end}`;

//   return getData(`${urlRoot}?${query}`);
// }

// useEffect(() => {
//   // POST request using axios inside useEffect React hook
//   const article = { title: 'React Hooks POST Request Example' };
//   axios.post('https://reqres.in/api/articles', article)
//       .then(response => setArticleId(response.data.id));

// // empty dependency array means this effect will only run once (like componentDidMount in classes)
// }, []);