function pass()
{
    document.getElementById('txtInsChar').value = document.getElementById('txtRandom').value
    document.getElementById('btnConfirm').click()
}

document.body.addEventListener('load', pass)
pass()