// Authorization token that must have been created previously. See : https://developer.spotify.com/documentation/web-api/concepts/authorization
const token = 'BQDyJvOAJEMgQ-HWwuqqW3vU-oINX5eUU_bU_TCiCA0yhD29eK7myxGvRCrZy0O4QSV69T9dktMr6DxncghJfUS_2bbfQ2j8uafgspg1ivIbSo3BJrmPtj9w_wXZ6kLVVP1zuGl7uJVA7s6SuUXgcnAr-9d2GNZRpuR_eyk1DW6Ybv5DL_pkcTC41qQCl0gcT9dLD-yFCD0MXi9tEYCRFqzn6OcF_96dhVWC0IDIUdzwq-Woit73PaSo1IM3JtfN69i2q62RxK9RLBhHd0a0quu4';
async function fetchWebApi(endpoint, method, body) {
  const res = await fetch(`https://api.spotify.com/${endpoint}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    method,
    body:JSON.stringify(body)
  });
  return await res.json();
}

async function getTopTracks(){
  // Endpoint reference : https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
  return (await fetchWebApi(
    'v1/me/top/tracks?time_range=long_term&limit=5', 'GET'
  )).items;
}

const topTracks = await getTopTracks();
console.log(
  topTracks?.map(
    ({name, artists}) =>
      `${name} by ${artists.map(artist => artist.name).join(', ')}`
  )
);