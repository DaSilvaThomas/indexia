// const typeLabels = {{ type_labels|safe }};
// const typeCounts = {{ type_counts|safe }};
// const commonWordsLabels = {{ common_words_labels|safe }};
// const commonWordsCounts = {{ common_words_counts|safe }};

// // Graphique par type de fichier
// new Chart(document.getElementById('fileTypeChart'), {
//     type: 'bar',
//     data: {
//         labels: typeLabels,
//         datasets: [{
//             label: 'Nombre de fichiers',
//             data: typeCounts,
//             backgroundColor: 'rgba(54, 162, 235, 0.6)'
//         }]
//     }
// });

// // Graphique des mots les plus fréquents
// new Chart(document.getElementById('commonWordsChart'), {
//     type: 'pie',
//     data: {
//         labels: commonWordsLabels,
//         datasets: [{
//             label: 'Fréquence',
//             data: commonWordsCounts,
//             backgroundColor: [
//                 'rgba(255, 99, 132, 0.6)',
//                 'rgba(54, 162, 235, 0.6)',
//                 'rgba(255, 206, 86, 0.6)',
//                 'rgba(75, 192, 192, 0.6)',
//                 'rgba(153, 102, 255, 0.6)',
//                 'rgba(255, 159, 64, 0.6)',
//             ]
//         }]
//     }
// });