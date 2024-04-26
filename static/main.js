console.log('salut')

const MAX_POINTS = 75;

const skillInputs = document.querySelectorAll('.ability-input');
const pointRestant = document.getElementById('pointRestant');

skillInputs.forEach(input => {
    input.addEventListener('change', function() {
        let totalPoints = 0;
        skillInputs.forEach(input => {
            totalPoints += Number(input.value);
        });

        if (totalPoints > MAX_POINTS) {
            this.value = this.value - (totalPoints - MAX_POINTS);
            totalPoints = MAX_POINTS;
        }
        
        pointRestant.textContent = MAX_POINTS - totalPoints;
    });
});

$('#roll-dice-button').click(function() {
    $.ajax({
        url: '/roll_dice',
        type: 'GET',
        success: function(data) {
            console.log(data);
            $('#dice-roll-result').text(data.dice_roll);
            $('#dice-roll-skill').text(data.skill);
        }
    });
});